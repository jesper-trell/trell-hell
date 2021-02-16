import React, { Component } from "react";

class LikeButtonApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      liked: true,
    };
  }

  componentDidMount() {
    fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
    .then(response => response.json())
    .then((data) => {
      this.setState({ likes: data })
    })
    .catch(console.log)
  }

  // render() {
  //   return (
  //     <Like liked={ this.state.liked } />
  //   )
  // }

  click_like = () => {
    this.setState({
      liked: !this.state.liked
    });
  }

  render() {
    if (this.state.liked) {
      return (
        <button onClick={this.click_like} type="submit" className="btn-link">Unlike</button>
      )
    }
    else {
      return (
        <button onClick={this.click_like} type="submit" className="btn-link">Like</button>
      )
    }
  }
}

// click_like = () => {
//   this.setState({
//     liked: !this.state.liked
//   });
// };

const Like = ({ liked }) => {
  if (liked) {
    return (
      <button type="submit" className="btn-link">Unlike</button>
    )
  }
  else {
    return (
      <button type="submit" className="btn-link">Like</button>
    )
  }
};

export { LikeButtonApp }