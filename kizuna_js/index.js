import ReactDOM from 'react-dom';
import React from 'react';
//import {entrypoint as new_reaction_image_entry} from "./containers/NewReactionImage";

// not DRY but IDGAF the perf benefits are worth it

const new_reaction_image_entry_el = document.getElementById('new-reaction-image');
if (new_reaction_image_entry_el) {
    import(
        /* webpackChunkName: "kizuna-new-reaction-image" */
        "./containers/NewReactionImage"
    ).then(module => {
        const {NewReactionImageContainer} = module;
        ReactDOM.render(<NewReactionImageContainer />, new_reaction_image_entry_el);
    })
}
