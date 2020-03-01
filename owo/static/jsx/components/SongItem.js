import React, {Component} from "react";
import ReactDOM from "react-dom";
import "./../../styles.css";
import unfilledLike from "../../../src/like_unfilled.png";
import filledLike from "../../../src/like_filled.png";

class SongItem extends Component {
    constructor() {
        super();
        this.state = {
            data: [],
            dataObjects: [],
            voted: [],
            elId: "",
            loggedIn: false
        };
    }

    componentDidMount() {
        this.getData();
        console.log(this.readCookie("access_token_cookie"));
        if (this.readCookie("access_token_cookie") !== "tipidor" || this.readCookie("isAdmin") !== "tipidor") {
            this.setState({loggedIn: true});
        }
    }

    getData() {
        fetch("/election/getlast/song")
            .then(response =>
                response.json()
            )
            .then(data => this.setState({data: data}))
            .catch(error => console.log(error));
    }

    getVoted() {
        if (this.state.loggedIn && this.state.elId !== "" && this.state.voted.length === 0) {
            fetch("/election/" + this.state.elId + "/voted")
                .then(response =>
                    response.json()
                )
                .then(data => this.setState({voted: data}))
                .catch(error => console.log(error));
        }
    }

    color(id) {
        if (this.state.voted.indexOf(id) > -1) {
            document.getElementById(id).src = filledLike;
        }
    }

    unvote(id) {
        fetch("/election/" + this.state.elId + "/unvote/" + id, {
            method: "POST",
            credentials: "include",
        }).catch(error => console.log(error));
        document.getElementById(id).src = unfilledLike;
        document.getElementById(id).nextElementSibling.innerText = parseInt(document.getElementById(id).nextElementSibling.innerText) - 1;
    }

    vote(id) {
        fetch("/election/" + this.state.elId + "/vote/" + id, {
            method: "POST",
            credentials: "include",
        }).catch(error => console.log(error));
        document.getElementById(id).src = filledLike;
        document.getElementById(id).nextElementSibling.innerText = parseInt(document.getElementById(id).nextElementSibling.innerText) + 1;
    }

    handleClick(id) {
        if (document.getElementById(id) !== null) {
            if (document.getElementById(id).src === unfilledLike) {
                this.vote(id);
            } else {
                this.unvote(id);
            }
        }
    }

    readCookie(name) {
        console.log(document.cookie);
        let nameEQ = name + "=";
        let ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) {
                console.log(c.substring(nameEQ.length, c.length));
                return c.substring(nameEQ.length, c.length);
            }
        }
        console.log("gay");
        return "tipidor";
    }

    render() {
        if (this.state.data.hasOwnProperty("electionInfo")) {
            document.getElementById("title_index").innerText = this.state.data["electionInfo"]["name"];
            if (this.state.elId === "") {
                this.setState((state) => {
                    return {elId: state.data["electionInfo"]["id"]}
                });
            }
            this.getVoted();
        }
        if (this.state.data.hasOwnProperty("normalObjects")) {
            if (this.state.dataObjects.length === 0) {
                let dataa = this.state.data["normalObjects"].sort((a, b) => a["voters"].length < b["voters"].length ? 1 : -1);
                this.setState({dataObjects: dataa});
            }
            if (this.state.loggedIn === true) {
                return (
                    <div className="songitems-container">
                        {this.state.dataObjects.map(item =>
                            <div className="songitem">
                                <div className="songitem-info">
                                    <div className="songitem-title"> {item["name"]} </div>
                                    <div className="songitem-singer"> {item["singer"]} </div>
                                </div>
                                <img src={unfilledLike} alt="icon" className="like-button" id={item["id"]}
                                     onClick={(e) => this.handleClick(item["id"], e)}/> {this.color(item['id'])}
                                <div className="votes-count">{item["voters"].length}</div>
                            </div>
                        )}
                    </div>)
            } else {
                return (
                    <div className="songitems-container">
                        {this.state.dataObjects.map(item =>
                            <div className="songitem">
                                <div className="songitem-info">
                                    <div className="songitem-title"> {item["name"]} </div>
                                    <div className="songitem-singer"> {item["singer"]} </div>
                                </div>
                                <img src={unfilledLike} alt="icon" className="like-button" id={item["id"]}/>
                                <div className="votes-count">{item["voters"].length}</div>
                            </div>
                        )}
                    </div>
                );
            }
        } else {
            return <div> Something has gone wrong (data) </div>;
        }
    }
}

export default SongItem;
const wrapper = document.getElementById("songs-container");
ReactDOM.render(<SongItem/>, wrapper);

/*<!--<div className="dropdown">
                                    <button className="dropdown-button" onClick={(e) => this.handleClickEdit(item["id"], e)}> Edit </button>
                                    <div className="dropdown-content">
                                        <form>
                                            <input type="text"/> Название <br/>
                                            <input type="text"/> Исполнитель <br/>
                                            <input type="checkbox"/> ban
                                        </form>
                                    </div>
                                </div>-->*/