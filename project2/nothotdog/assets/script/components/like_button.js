import React, { Component } from "react";


class LikeButtonApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      liked: false,
      buttonText: 'Like',
    };
  }

  componentDidMount() {
    this.initialState()
  }

  initialState = () => {
    for (let like of this.props.likes) {
      console.log(like.user.id)
      if (like.user.id == context.currentUserID) {
        this.setState({liked: true})
        break;
      } else {
        this.setState({liked: false})
      }
    }
  }

  click_like = () => {
    console.log('Like button pressed')
    if (!this.state.liked) {
      this.setState({ buttonText: 'Unlike' });
      this.props.likeAction({method: 'POST'})
      console.log("Added a like")
    } else if (this.state.liked) {
      this.setState({ buttonText: 'Like' });
      this.props.likeAction({method: 'DELETE'})
      console.log("Removed a like")
    }

    this.setState({
      liked: !this.state.liked
    });
  }

  render() {
    return (
      <button onClick={ this.click_like } type="submit" className="btn-link">{ this.state.buttonText }</button>
    )
  }
}

export default LikeButtonApp