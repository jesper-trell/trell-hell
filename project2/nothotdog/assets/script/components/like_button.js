import React, { Component } from "react";
import get_cookie from '../get_cookie';

class LikeButtonApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      liked: true,
    };
  }

  componentDidMount() {
    this.setState(
      {
        liked: true,
      }
    )
    // fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
    //   .then(response => response.json())
    //   .then((data) => {
    //     this.setState({
    //       likes: data,
    //     })
    //   })
    //   .catch(console.log)
  }

  click_like = () => {
    this.setState({
      liked: !this.state.liked
    });

    if (!this.state.liked) {
      console.log("Added a like.")
      const csrftoken = get_cookie('csrftoken');
      fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like', {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        }
      })
    } else if (this.state.liked) {
      console.log("Removed a like.")
    }
  }

  render() {
    if (this.state.liked) {
      return (
        <button onClick={this.click_like} type="submit" className="btn-link">Unlike</button>
        // <button onClick={this.click_like} type="submit" className="btn-link">Unlike</button>
      )
    } else {
      return (
        <button onClick={this.click_like} type="submit" className="btn-link">Like</button>
        // <button onClick={this.click_like} type="submit" className="btn-link">Like</button>
      )
    }
  }
}

export default LikeButtonApp