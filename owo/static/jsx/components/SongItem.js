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
            voted: [],
            elId: "",
            loggedIn: false
        };
    }

    componentDidMount() {
        this.getData();
        if (document.cookie.hasOwnProperty("access_token_cookie")) {
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
        if (this.state.voted.hasOwnProperty("ids") && this.state.voted["ids"].indexOf(id) > -1) {
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

    render() {
        if (this.state.data.hasOwnProperty("electionInfo")) {
            if (this.state.elId === "") {
                this.setState((state) => {
                    return {elId: state.data["electionInfo"]["id"]}
                });
            }
            this.getVoted();
        }
        if (this.state.data.hasOwnProperty("normalObjects")) {
            if (this.state.loggedIn) {
                return (
                    <div className="songitems-container">
                        {this.state.data["normalObjects"].map(item =>
                            <div className="songitem">
                                <div className="songitem-info">
                                    <div className="songitem-title"> {item["name"]} </div>
                                    <div className="songitem-singer"> {item["singer"]} </div>
                                </div>
                                <img src={unfilledLike} alt="icon" className="like-button" id={item["id"]}
                                     onClick={(e) => this.handleClick(item["id"], e)}/> {this.color(item['id'])}
                                <div className="votes-count">{item["votes"]}</div>
                            </div>
                        )}
                    </div>)
            } else {
                return (
                    <div className="songitems-container">
                        {this.state.data["normalObjects"].map(item =>
                            <div className="songitem">
                                <div className="songitem-info">
                                    <div className="songitem-title"> {item["name"]} </div>
                                    <div className="songitem-singer"> {item["singer"]} </div>
                                </div>
                                <img src={unfilledLike} alt="icon" className="like-button" id={item["id"]}/>
                                <div className="votes-count">{item["votes"]}</div>
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