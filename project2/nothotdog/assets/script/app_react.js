import React, { Component } from "react";
import { render } from "react-dom";
import LikesApp from './components/likes';
import LikeButtonApp from './components/like_button';


class Pagination extends Component {
  render() {
    return (
      <div className="pagination-container">
        <form method="GET">
          <select name="paginate_by">
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="30">30</option>
          </select>
          <input type="submit" value="Paginate"/>
        </form>
      </div>
    )
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // data: [],
      // likes: this.updateLikes(),
      likes: []
      // loaded: false,
      // placeholder: "Loading"
    };
    console.log('running the parent constructor')
    this.updateLikes()
    // data2 = this.getLikes()
    console.log(this.getLikes())
    // console.log(data2)
  }

  // componentDidMount() {
  //   fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
  //     .then(response => response.json())
  //     .then((data) => {
  //       this.setState({ likes: data })
  //       // return data
  //     })
  //     .catch(console.log)
  // }

  getLikes = () => {
    fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
      .then(response => response.json())
      .then((data) => {
        return data;
      })
      // .catch(console.log)
  }

  updateLikes = () => {
    fetch('http://127.0.0.1:8000/baf55abd-8e54-4eba-b61f-a1ae61008cf5/like')
      .then(response => response.json())
      .then((data) => {
        this.setState({ likes: data })
      })
      .catch(console.log)
  }

  render() {
    console.log("rendering parent")
    console.log(this.state.likes)
    return (
      <div>
        <LikesApp likes={ this.state.likes } />
        <LikeButtonApp updateLikes={ this.updateLikes } likes={ this.state.likes } />
      </div>
    );
  }
}

const container = document.getElementById('app');
if (container) {
  render(<App />, container);
}

const pagination_container = document.getElementById('pagination');
if (pagination_container) {
  render(<Pagination />, pagination_container);
}

// const likes_container = document.getElementById('likes-container');
// if (likes_container) {
//   render(<LikesApp />, likes_container);

// }

// const like_button_container = document.getElementById('like-button-container');
// if (like_button_container) {
//   render(<LikeButtonApp />, like_button_container);
// }

export default App