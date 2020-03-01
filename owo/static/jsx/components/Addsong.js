import React, {Component} from "react";
import ReactDOM from "react-dom";
import "./../../styles.css";

class AddSong extends Component {
    constructor() {
        super();
        this.state = {
            data: []
        };
    }

    sendData() {
        if (document.getElementById("input-song-title").checkValidity() === false ||
            document.getElementById("input-song-author").checkValidity() === false) {
            document.getElementById("required-alert").style.display = "block";
            return;
        } else {
            document.getElementById("required-alert").style.display = "none";
        }
        if (!this.state.data.hasOwnProperty("electionInfo")) {
            this.getData();
        }
        console.log("JAVASCRIPT ПОМОЙКА");
        let electionUid = this.state.data["electionInfo"]["id"];
        let name = document.getElementById("input-song-title").value;
        let singer = document.getElementById("input-song-author").value;
        fetch("/election/" + electionUid + "/vote/new", {
            method: "POST",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                type: "song",
                singer: singer,
                cutCommentary: "",
                album: "",
                serviceLink: ""
            })
        }).catch(error => console.log(error));
        document.getElementById("added-alert").style.display = "block";
    }

    getData() {
        fetch("/election/getlast/song")
            .then(response => response.json())
            .then(data => this.setState({data: data}))
            .catch(error => console.log(error));
    }

    componentDidMount() {
        this.getData();
    }

    render() {
        return (
            <div>
                <form className="add-song">
                    <div className="form-label-group add-song-input-container">
                        <input type="text" id="input-song-title" className="form-control add-song-input"
                               name="title" placeholder="Название песни" required autoFocus/>
                    </div>

                    <div className="form-label-group add-song-input-container">
                        <input type="text" id="input-song-author" className="form-control add-song-input"
                               name="author" placeholder="Исполнитель" required/>
                    </div>

                    <div className="form-label-group add-song-input-container">
                        <input type="text" className="form-control add-song-input" name="link"
                               placeholder="Яндекс.Музыка, YouTube и т.п."/>
                    </div>

                    <div className="form-label-group add-song-input-container">
                        <input type="text" className="form-control add-song-input" name="cut"
                               placeholder="Обрезка трека"/>
                    </div>
                    <button type="button" className="add-item-submit" onClick={() => this.sendData()}>Добавить</button>
                </form>
                <div className="required-alert" id="required-alert">
                    Пожалуйста, заполните поля названия и исполнителя
                </div>
                <div className="added-alert" id="added-alert">
                    Песня добавлена
                </div>
            </div>)
    }
}

export default AddSong;
const wrapper = document.getElementById("addsong-container");
ReactDOM.render(<AddSong/>, wrapper);