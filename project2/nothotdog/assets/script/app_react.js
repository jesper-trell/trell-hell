import React, { Component } from "react";
import { render } from "react-dom";
import LikesApp from './components/likes';
import LikeButtonApp from './components/like_button';
import get_cookie from './get_cookie';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      likes: [],
      loaded: false,
    };
  }

  componentDidMount() {
    fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
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
    fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
      .then(response => response.json())
      .then((data) => {
        this.setState({
          likes: data,
        })
      })
      .catch(console.log)
  }

  likeAction = ({method}) => {
    const csrftoken = get_cookie('csrftoken');
    fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like', {
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