import React, { Component } from "react";
import { render } from "react-dom";
import { ContactsApp } from './components/contacts';
import { LikesApp } from './components/likes';


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
      <ul>
        {this.state.data.map(photo => {
          return (
            <img key={ photo.id } src={ photo.image } alt={ photo.uu_id } style={ {width:300, height:200} }/>
          );
        })}
      </ul>
    );
  }
}

const container = document.getElementById('app');
render(<App />, container);

const pagination_container = document.getElementById('pagination');
render(<Pagination />, pagination_container);

const test_container = document.getElementById('test-container');
render(<ContactsApp />, test_container);

const likes_container = document.getElementById('likes-container');
render(<LikesApp />, likes_container);

export default App