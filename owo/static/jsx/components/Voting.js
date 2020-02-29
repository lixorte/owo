import React, {Component} from "react";
import ReactDOM from "react-dom";
import "./../../styles.css";
import unfilledLike from "../../../src/like_unfilled.png";

class Voting extends Component {
    constructor() {
        super();
        this.state = {
            songdata: [],
            topicdata: [],
            songitems: [],
            data: [],
            opened: "",
            elId: "",
            itemId: ""
        }
    }

    newVoting(e) {
        if (document.getElementById("voting-text").checkValidity() === false || document.getElementsByName("state")[0] === false &&
            document.getElementsByName("state")[1] === false || document.getElementsByName("type")[0] === false &&
            document.getElementsByName("type")[1] === false) {
            document.getElementById("required-alert-vote").style.display = "block";
            return;
        }
        document.getElementById("required-alert-vote").style.display = "none";
        let name = document.getElementById("voting-text").value;
        let states = document.getElementsByName("state");
        let state, type;
        for (let i = 0; i < states.length; ++i) {
            if (states[i].checked) {
                state = states[i].value;
            }
        }
        let types = document.getElementsByName("type");
        for (let i = 0; i < types.length; ++i) {
            if (types[i].checked) {
                type = types[i].value;
            }
        }
        fetch("/election/new", {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                state: state,
                type: type
            })
        }).catch(error => console.log(error));
    }

    getSongData() {
        fetch("/election/find/song", {
        })
            .then(response => response.json())
            .then(data => this.setState({songdata: data}))
            .catch(error => console.log(error))
    }

    getTopicData() {
        fetch("/election/find/topic", {
        })
            .then(response => response.json())
            .then(data => this.setState({topicdata: data}))
            .catch(error => console.log(error))
    }

    handleClickChoose(type, e) {
        if (type === "song") {
            if (document.getElementById("show-song-btn").innerText === "Показать голосования за песни") {
                document.getElementById("show-song-btn").innerText = "Скрыть голосования за песни";
                this.getSongData();
            } else {
                document.getElementById("show-song-btn").innerText = "Показать голосования за песни";
                this.setState({songdata: []});
            }
        } else {
            if (document.getElementById("show-topic-btn").innerText === "Показать голосования за темы") {
                document.getElementById("show-topic-btn").innerText = "Скрыть голосования за темы";
                this.getTopicData();
            } else {
                document.getElementById("show-topic-btn").innerText = "Показать голосования за темы";
                this.setState({topicdata: []});
            }
        }
    }

    votingStatus(state) {
        if (state === "ongoing") {
            return "Активное";
        }
        if (state === "freezed") {
            return "Замороженное";
        }
        return "Завершенное";
    }

    handleClickDelete(id, e) {
        fetch("/election/" + id + "/delete", {
            method: "POST",
            credentials: "include",
        }).catch(error => console.log(error))
    }

    handleClickOpen(id, e) {
        fetch("/election/" + id)
            .then(response =>
                response.json()
            )
            .then(data => this.setState({data: data}))
            .catch(error => console.log(error));
        if (this.state.data.hasOwnProperty("normalObjects")) {
            if (this.state.songitems.length !== 0) {
                this.setState({songitems: [], opened: ""});
            } else {
                this.setState({songitems: this.state.data["normalObjects"], opened: id});
            }
        }
        console.log(this.state.data);
    }

    handleClickEdit(elId, itemId) {
        document.getElementsByClassName("edit-option")[0].style.display = "block";
        this.setState({elId: elId, itemId: itemId});
    }

    submitEditData() {
        let title = document.getElementById(this.state.itemId).innerText,
            singer = document.getElementById(this.state.itemId).nextElementSibling.innerText, ban = "normal";
        if (document.getElementById("option-title").value !== "") {
            title = document.getElementById("option-title").value;
        }
        if (document.getElementById("option-singer").value !== "") {
            singer = document.getElementById("option-singer").value;
        }
        if (document.getElementById("banochka").checked === true) {
            ban = "banned";
        }
        console.log(title, singer, ban);
        fetch("/election/" + this.state.elId + "/vote/" + this.state.itemId, {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: title,
                singer: singer,
                album: "",
                state: ban
            })
        });
        document.getElementsByClassName("edit-option")[0].style.display = "none";
    }

    renderItems(name, singer, votes, itemId, elId, type) {
        if (elId === this.state.opened) {
            if (type === "song") {
                return (
                    <div className="songitem">
                        <form className="songitem-info">
                            <div className="songitem-title" id={itemId}> {name} </div>
                            <div className="songitem-singer"> {singer} </div>
                        </form>
                        <div className="like-button edit-button" onClick={() => {
                            this.handleClickEdit(elId, itemId)
                        }}> Edit
                        </div>
                        <div className="votes-count">{votes}</div>
                    </div>
                )
            } else {
                return (
                    <div className="songitem">
                        <div className="songitem-info">
                            <div className="theme-title" id={itemId}> {name} </div>
                        </div>
                        <div className="like-button" onClick={() => {
                            this.handleClickEdit(elId, itemId)
                        }}> Edit
                        </div>
                        <div className="votes-count">{votes}</div>
                    </div>
                )
            }
        }
    }

    render() {
        return (
            <div>
                <form className="add-song">
                    <div className="add-song-input-container">
                        <input type="text" id="voting-text" className="new-voting-input-text form-control"
                               placeholder="Название голосования" required/>
                    </div>
                    <div className="add-song-input-container">
                        <input type="radio" name="state" value="ongoing" required/> Активное <br/>
                        <input type="radio" name="state" value="freezed" disabled required/> Замороженное <br/>
                    </div>
                    <div className="add-song-input-container">
                        <input type="radio" name="type" value="song" required/> Песни <br/>
                        <input type="radio" name="type" value="topic" required/> Темы <br/>
                    </div>
                </form>
                <div className="required-alert" id="required-alert-vote"> Пожалуйста, заполните все поля</div>
                <br/>
                <button className="new-voting" onClick={(e) => this.newVoting(e)}> Новое голосование</button>
                <br/>
                <button className="new-voting new-voting-show" id="show-song-btn"
                        onClick={(e) => this.handleClickChoose("song", e)}>
                    Показать голосования за песни
                </button>
                <div className="edit-option">
                    <form className="add-song" style={{background: "white", paddingTop: "30px"}}>
                        <div onClick={() => {
                            document.getElementsByClassName("edit-option")[0].style.display = "none"
                        }} className="close-button">X</div>
                        <div className="add-song-input-container">
                            <input type="text" id="option-title" className="new-voting-input-text form-control edit-input"
                                   placeholder="Название"/>
                            <input type="text" id="option-singer" className="new-voting-input-text form-control edit-input"
                                   placeholder="Исполнитель"/>
                        </div>
                        <div className="add-song-input-container">
                            <input id="banochka" type="checkbox" value="banned"/> Заблокировать <br/>
                        </div>
                    </form>
                    <br/>
                    <button className="add-item-submit" style={{width: "140px"}} onClick={() => {
                        this.submitEditData()
                    }}> Редактировать
                    </button>
                </div>
                {this.state.songdata.map(item =>
                    <div>
                        <div className="voting-item">
                            <div className="voting-info" onClick={() => this.handleClickOpen(item["id"])}>
                                <div className="voting-title">{item["name"]}</div>
                                <div className="voting-status">{this.votingStatus(item["state"])}</div>
                            </div>
                        </div>
                        <div className="songitems-container">
                            {this.state.songitems.map(songitem =>
                                this.renderItems(songitem["name"], songitem["singer"], songitem["votes"], songitem["id"], item["id"], item["type"])
                            )}
                        </div>
                    </div>
                )}
                <br/>
                <button className="new-voting new-voting-show" id="show-topic-btn"
                        onClick={() => this.handleClickChoose("topic")}>
                    Показать голосования за темы
                </button>
                {this.state.topicdata.map(item =>
                    <div>
                        <div className="voting-item">
                            <div className="voting-info" onClick={() => this.handleClickOpen(item["id"])}>
                                <div className="voting-title">{item["name"]}</div>
                                <div className="voting-status">{this.votingStatus(item["state"])}</div>
                            </div>
                        </div>
                        <div className="songitems-container">
                            {this.state.songitems.map(themeitem =>
                                this.renderItems(themeitem["name"], "", themeitem["votes"], themeitem["id"], item["id"], item["type"])
                            )}
                        </div>
                    </div>
                )}
            </div>
        )
    }
}

export default Voting;
const wrapper = document.getElementById("voting-container");
ReactDOM.render(<Voting/>, wrapper);

/*<input type="text" className="new-voting-input-text form-control" placeholder="Статус голосования"/>
<input type="text" className="new-voting-input-text  form-control" placeholder="Темы или песни"/>
<div className="delete-button" onClick={() => this.handleClickDelete(item["id"])}>
                                Delete
                            </div>*/