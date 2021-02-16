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
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("photos_API")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <div>
        <LikesApp />
        <LikeButtonApp />
        {/* <LikeButtonApp items={displayedItems} /> */}
      </div>
    );

    // return (
    //   <ul>
    //     {this.state.data.map(photo => {
    //       return (
    //         <img key={ photo.id } src={ photo.image } alt={ photo.uu_id } style={ {width:300, height:200} } />
    //       );
    //     })}
    //   </ul>
    // );
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