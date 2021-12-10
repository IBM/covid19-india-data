import React from 'react';
import { TASKS } from './tasks.js';
import { generateURL } from '../../components/Info';
import { Link, Button, Tile, Tag } from 'carbon-components-react';

const Task = props => (
  <Tile className="task-tile">
    <img
      alt="Task"
      src={generateURL(props.props.imageURL, 'png', '/tasks')}
      width="100%"
    />

    <div style={{ padding: '20px' }}>
      <div className="topic-tags">
        <div />
        {props.props.topics.map((item, index) => (
          <Tag key={index} type="purple" className="flattened-tag">
            {item}
          </Tag>
        ))}

        <Tag type={props.props.difficulty.color} className="flattened-tag">
          {props.props.difficulty.level}
        </Tag>

        {props.props.states.map((item, index) => (
          <Tag key={index} type="gray" className="flattened-tag">
            {item}
          </Tag>
        ))}
      </div>
      <br />

      <h5>{props.props.title}</h5>
      <br />

      <p style={{ fontSize: 'inherit' }}> {props.props.description}</p>
    </div>
    {props.props.url && (
      <Link className="button-generic" href={props.props.url} target="_blank">
        <Button size="small">Learn more</Button>
      </Link>
    )}
  </Tile>
);

class TasksPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <>
        <div
          className="bx--grid bx--grid--full-width bx--container"
          style={{ width: '100%', paddingBottom: '100px' }}>
          <div className="bx--col-lg-16">
            <br />

            <div className="bx--row">
              <div className="bx--col-lg-12">
                <div className="bx--row">
                  {Array.from(Array(4).keys()).map(e => {
                    return (
                      <div key={e} className="bx--col-lg-5">
                        {TASKS.map((item, index) => {
                          if (item.column === e)
                            return <Task key={index} props={item} />;
                        })}
                      </div>
                    );
                  })}
                </div>
              </div>
              <div className="bx--col-lg-4">
                <h3>Datathon @ IndoML 2021</h3>
                <hr />

                <p>
                  IndoML is a pan-India symposium aimed at undergraduate and
                  graduate students in Indian universities to participate in
                  structured artificial intelligence, machine learning, and data
                  science tasks.
                </p>

                <br />
                <Link
                  href="https://www.kaggle.com/dataset/cb06e66c26c46ed9e701be6750e08f956d63c91d1be2bc633d19e201c7704c5b"
                  target="_blank"
                  className="no-decoration">
                  <Button kind="secondary" size="small">
                    Participate
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </>
    );
  }
}

export default TasksPage;
