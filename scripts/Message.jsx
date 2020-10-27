import React from 'react';
import PropTypes from 'prop-types';
import './Messagestyles.css';
import botpfp from './botpfp.png';

function Message({
  text, user, reader, pfp_url,
}) {
  function createMarkup() {
    return { __html: { text }.text };
  }
  function createImg() {
    return { __html: { pfp_url }.pfp_url };
  }

  if (user === reader) {
    return (
      <div className="msg-user">

        <div className="user-pfp-self">
          <div className="pfp" dangerouslySetInnerHTML={createImg()} />
          <div className="self-tag">{user}</div>
        </div>

        <div className="clear"> </div>
        <div className="bubble-container ">
          <div className="bubble self" dangerouslySetInnerHTML={createMarkup()} />
        </div>
      </div>
    );
  }
  if (user === 'Bot') {
    return (
      <div className="msg-user">

        <div className="user-pfp-other">
          <div className="pfp"><img src={botpfp} alt="The Cutest Bot Ever" /></div>
          <div className="user-tag-container-other">Paimon (Emergency Food) [Bot]</div>
        </div>

        <div className="bubble-container">
          <div className="bubble bot" dangerouslySetInnerHTML={createMarkup()} />
        </div>
      </div>
    );
  }

  return (
    <div className="msg-user">

      <div className="user-pfp-other">
        <div className="pfp" dangerouslySetInnerHTML={createImg()} />
        <div className="user-tag-container-other">{user}</div>
      </div>

      <div className="bubble-container">
        <div className="bubble incoming" dangerouslySetInnerHTML={createMarkup()} />
      </div>
    </div>
  );
}

Message.propTypes = {
  text: PropTypes.string.isRequired,
  user: PropTypes.string.isRequired,
  reader: PropTypes.string.isRequired,
  pfp_url: PropTypes.string.isRequired,
};

export default Message;
