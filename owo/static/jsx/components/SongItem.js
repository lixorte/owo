import React, {Component} from "react";
import ReactDOM from "react-dom";
import "./../../styles.css";
import unfilledLike from "../../../src/like_unfilled.png";
import filledLike from "../../../src/like_filled.png";

const address = "http://0.0.0.0";

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
        if (document.cookie.hasOwnProperty("JWT") || 1) {
            this.setState({loggedIn: true});
        }
    }

    getData() {
        fetch(address + "/election/getlast/song")
            .then(response =>
                response.json()
            )
            .then(data => this.setState({data: data}))
            .catch(error => console.log(error));
    }

    getVoted() {
        if (this.state.loggedIn && this.state.elId !== "" && this.state.voted.length === 0) {
            fetch(address + "/election/" + this.state.elId + "/voted")
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

    vote(id) {
        fetch(address + "/election/" + this.state.elId + "/vote/" + id, {
            method: "POST",
            credentials: "include",
            mode: 'no-cors'
        }).catch(error => console.log(error));
        if (document.getElementById(id) !== null) {
            if (document.getElementById(id).src === unfilledLike) {
                document.getElementById(id).src = filledLike;
            } else {
                document.getElementById(id).src = unfilledLike;
            }
        }
    }

    handleClick(id) {
        this.vote(id);
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
                                <img src={unfilledLike} alt="icon" className="like-button" id={item["id"]}
                                     onClick={function () {
                                         if (document.getElementById(item["id"]).src === unfilledLike) {
                                             document.getElementById(item["id"]).src = filledLike;
                                         } else {
                                             document.getElementById(item["id"]).src = unfilledLike;
                                         }
                                     }}/>
                            </div>
                        )}
                    </div>
                );
            }
        } else {
            return <div> Something has gone wrong </div>;
        }
    }
}

export default SongItem;
const wrapper = document.getElementById("songs-container");
ReactDOM.render(<SongItem/>, wrapper);
