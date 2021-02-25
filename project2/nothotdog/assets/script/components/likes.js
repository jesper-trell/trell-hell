import React, { Component } from 'react';

class LikesApp extends Component {
  render() {
    console.log(this.props.likes);
    return (
      <Likes likes={ this.props.likes } />
    )
  }
}

const Likes = ({ likes }) => {
  return(
  <div>
    {/* <center><h1>Contact List</h1></center> */}
    <span>
      Likes:
      { likes.length }
      <br />
    </span>
    <span>Liked by: </span>
    {likes.map((like) => (
      <div style={{ display: 'inline-block' }} key={ like.user.id }>
        <p key={ like.user.id }>
          { like.user.username }
          ,
        </p>
      </div>
    ))}
  </div>
  )
};

export default LikesApp;
