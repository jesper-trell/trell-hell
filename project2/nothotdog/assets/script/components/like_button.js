import React, { Component } from "react";


var containerData = document.querySelector('#app');
if (containerData) {
  var userid = containerData.dataset.userid;
}

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
      console.log(userid)
      if (like.user.id == userid) {
        this.setState({liked: true})
        this.setState({buttonText: 'Unlike'})
        break;
      } else {
        this.setState({liked: false})
        this.setState({buttonText: 'Like'})
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