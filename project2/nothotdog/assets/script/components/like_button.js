import React, { Component } from "react";
import get_cookie from '../get_cookie';

class LikeButtonApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      liked: false,
    };
    this.initialState()
  }

  componentDidMount() {
    console.log("finished rendering like button")
    console.log(this.props.likes)
  }

  initialState = () => {
    console.log('init state called')
    this.props.likes.map(like => {
      console.log(like.user.id)
      if (like.user.id == context.currentUserID) {
        console.log('exists')
        this.setState({liked: true})
      } else {
        console.log('not exists')
        this.setState({liked: false})
      }
    })
  }

  click_like = () => {
    console.log('button pressed')
    this.props.updateLikes();

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

    this.setState({
      liked: !this.state.liked
    });
  }

  render() {
    console.log('rendering like_button')
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