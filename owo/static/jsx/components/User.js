import React, {Component} from "react";
import ReactDOM from "react-dom";
import "./../../styles.css";
import rightArrow from "../../../src/arrow_right.png";
import leftArrow from "../../../src/arrow_left.png";


function min(a, b) {
    if (a < b) {
        return a;
    }
    return b;
}

function max(a, b) {
    if (a > b) {
        return a;
    }
    return b;
}

class User extends Component {
    constructor() {
        super();
        this.state = {
            data: [],
            items: [],
            page: 0,
            filter: "none"
        };
    }

    componentDidMount() {
        this.getData();
        if (this.state.data.length !== 0) {
            this.state.items = this.state.data.slice(0, 25);
        }
    }

    getData() {
        fetch("/user")
            .then(response => response.json())
            .then(data => this.setState({data: data}))
            .catch(error => console.log(error));
    }

    handleClickRight(e) {
        let maxpage = Math.ceil(this.state.data.length / 25) - 1;
        if (this.state.page === maxpage) {
            return;
        }
        let sliced = this.state.data.slice((this.state.page + 1) * 25, min((this.state.page + 1) * 25 + 25, this.state.data.length));
        let newpage = this.state.page + 1;
        this.setState({items: sliced, page: newpage});
    }

    handleClickLeft(e) {
        if (this.state.page === 0) {
            return;
        }
        let sliced = this.state.data.slice((this.state.page - 1) * 25, this.state.page * 25);
        let newpage = this.state.page - 1;
        this.setState({items: sliced, page: newpage});
    }

    updateUser(user, upd, id, e) {
        if (upd === "type") {
            let type = user["type"] === "admin" ? "normal" : "admin";
            if (document.getElementById(id).innerText === "Повысить") {
                document.getElementById(id).innerText = "Понизить";
            } else {
                document.getElementById(id).innerText = "Повысить";
            }
            fetch("/user/" + user["name"], {
                method: "POST",
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: type,
                    state: user["state"]
                })
            }).catch(error => console.log(error));
        }
        if (upd === "state") {
            let state = user["state"] === "ok" ? "banned" : "ok";
            if (document.getElementById(id).nextElementSibling.innerText === "Забанить") {
                document.getElementById(id).nextElementSibling.innerText = "Разбанить";
            } else {
                document.getElementById(id).nextElementSibling.innerText = "Забанить";
            }
            fetch("/user/" + user["name"], {
                method: "POST",
                credentials: "include",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: user["type"],
                    state: state
                })
            }).catch(error => console.log(error));
        }
    }

    isAdmin(type) {
        if (type === "admin") {
            return "Понизить";
        } else {
            return "Повысить";
        }
    }

    isBanned(state) {
        if (state === "normal") {
            return "Забанить";
        } else {
            return "Разбанить";
        }
    }

    render() {
        if (this.state.data.length === 0) {
            this.getData();
        }
        if (this.state.data.length !== 0 && this.state.items.length === 0) {
            this.state.items = this.state.data.slice(0, 25);
        }
        if (this.state.items.length !== 0) {
            return (
                <div className="user-container">
                    {this.state.items.map(item =>
                        <div>
                            <div className="user-item">
                                <div className="user-info">
                                    <div className="user-name"> {item["name"]} </div>
                                </div>
                            </div>
                            <button className="user-promote" id={item["id"]}
                                 onClick={(e) => this.updateUser(item, "type", item["id"], e)}> {this.isAdmin(item["type"])}
                            </button>
                            <button className="user-ban"
                                 onClick={(e) => this.updateUser(item, "state", item["id"], e)}> {this.isBanned(item["type"])}
                            </button>
                        </div>
                    )}
                    <div className="user-buttons-container">
                        <img src={leftArrow} className="user-button-left user-button" alt="left" onClick={(e) => this.handleClickLeft(e)}/>
                        <img src={rightArrow} className="user-button-right user-button" alt="right" onClick={(e) => this.handleClickRight(e)}/>
                    </div>
                </div>
            )
        } else {
            return (
                <div>Data is lost sorry</div>
            )
        }
    }
}

export default User;
const wrapper = document.getElementById("users-container");
ReactDOM.render(<User/>, wrapper);