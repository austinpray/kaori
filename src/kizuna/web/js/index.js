import ReactDOM from 'react-dom';
import React from 'react';
import URI from 'urijs';
import localforage from 'localforage';
import _every from "lodash/every";

const STORE_NAME = 'kizuna';

function initStorage() {
  const store = localforage.createInstance({
    name: STORE_NAME
  });
  const result = {
    store,
    auth: null
  };
  const uri = new URI(window.location.href);
  const {auth} = uri.search(true);
  return new Promise(function (resolve, reject) {
    if (auth) {
      return store.setItem('auth', auth)
        .then(() = > resolve({...result, auth
    }))
    .
      catch(() = > resolve(result)
    )
    }
    return store.getItem('auth')
      .then(function (auth) {
        if (auth) {
          return resolve({...result, auth
        })
        }

        return resolve(result);
      })
      .catch(() = > resolve(result)
  )
  });
}

// below is not DRY but IDGAF the perf benefits are worth it

const new_reaction_image_entry_el = document.getElementById('new-reaction-image');
if (new_reaction_image_entry_el) {
  import(
    /* webpackChunkName: "kizuna-new-reaction-image" */
    "./containers/NewReactionImage"
    ).then(module = > {
    const {NewReactionImageContainer} = module;
  initStorage().then(function (storage) {
    ReactDOM.render( < NewReactionImageContainer
    {...
      storage
    }
    />, new_reaction_image_entry_el);
  });
})
}

// just a regular page with no react components
// still grab the auth key from url and save it
const entry_elements = [
  new_reaction_image_entry_el
];
if (_every(entry_elements, element = > !element))
{
  initStorage();
}
