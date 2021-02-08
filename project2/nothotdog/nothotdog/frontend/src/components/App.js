import React, { Component } from "react";
import { render } from "react-dom";

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
            <div>{photo.title} - {photo.description} - {photo.image} - {photo.image.url} - {photo.user} - {photo.pub_date} - {photo.flagged} - {photo.uu_id}</div>
            // <li key={photo.id}>
            //   {photo.title} - {photo.description}
            // </li>

            // <img src={photo.image.url} alt={photo.title} style="width:300px;height:200px;"></img>
            // <figure>
            //     <img src="{photo.image.url}" alt="{photo.uu_id}" style="width:300px;height:200px;"></img>
            //     <figcaption class="image-label"><a href="{photo.uu_id}"></a></figcaption>
            // </figure>
          );
        })}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);