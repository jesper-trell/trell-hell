import React, { Component } from "react";


class LikesApp extends Component {
  render() {
    return (
      <Likes likes={ this.props.likes } />
    )
  }
}

const Likes = ({ likes }) => {
  return (
    <div>
      {/* <center><h1>Contact List</h1></center> */}
      <span>Likes: { likes.length } <br/> </span>
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