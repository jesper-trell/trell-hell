import React, { Component } from "react";

class LikesApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      likes: []
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

  render() {
    return (
      <Likes likes={ this.state.likes } />
    )
  }
}

const Likes = ({ likes }) => {
    return (
      <div>
        {/* <center><h1>Contact List</h1></center> */}
        <span>Liked by: </span>
        {likes.map(like => (
          <div style={ {display:'inline-block'} }>
            <p>{ like.user.username },</p>
          </div>
        ))}
      </div>
    )
};

export default LikesApp