import React, { Component } from "react";
import { render } from "react-dom";
import LikesApp from './components/likes';
import LikeButtonApp from './components/like_button';
import get_cookie from './get_cookie';


var containerData = document.querySelector('#app');
if (containerData) {
  var uuid = containerData.dataset.uuid;
  var stringAPI = uuid + '/like';
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      likes: [],
      loaded: false,
    };
  }

  componentDidMount() {
    fetch(stringAPI)
      .then(response => response.json())
      .then((data) => {
        this.setState({
          likes: data,
          loaded: true
        })
      })
      .catch(console.log)
  }

  updateLikes = () => {
      fetch(stringAPI)
      .then(response => response.json())
      .then((data) => {
        this.setState({
          likes: data,
        })
      })
      .catch(console.log)
  }

  likeAction = ({ method }) => {
    const csrftoken = get_cookie('csrftoken');
    fetch(stringAPI, {
      credentials: 'same-origin',
      method: method,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      }
    })
      .then(() => {
        this.updateLikes();
      })
  }

  render() {
    return (
      <div>
        { this.state.loaded ? <LikesApp likes={ this.state.likes } /> : <h1> Loading </h1> }
        { this.state.loaded ? <LikeButtonApp likeAction={ this.likeAction } updateLikes={ this.updateLikes } likes={ this.state.likes } /> : <h1> Loading </h1> }
      </div>
    );
  }
}

const container = document.getElementById('app');
if (container) {
  render(<App />, container);
}

export default App