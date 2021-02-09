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
            // <div>{photo.image}</div>
            <div>{photo.title} - {photo.description} - {photo.image} - {photo.pub_date} - {photo.flagged.toString()} - {photo.uu_id} - {photo.username} -</div>
            // <img src="../../../../media/images/13023.jpg" style="width:300px;height:200px;" />
            // <img src={require(photo.image)} style="width:300px;height:200px;" />
            // <img src={photo.image} alt="{photo.uu_id}" style="width:300px;height:200px;"/>
          );
        })}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);