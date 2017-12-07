import React, {Component} from 'react';
import {ReactionImage} from "../models/ReactionImage";
import Dropzone from "react-dropzone"
import _set from "lodash/set";
import _uniq from "lodash/uniq";
import _forEach from "lodash/forEach";
import _filter from "lodash/filter";
import _difference from "lodash/difference";
import _map from "lodash/map";
import _union from "lodash/union";
import TagsInput from 'react-tagsinput';
import Autosuggest from 'react-autosuggest';

import 'react-tagsinput/react-tagsinput.css'
import "./NewReactionImage.css"

import {GoCloudUpload, GoChevronLeft} from 'react-icons/lib/go';

export class NewReactionImageContainer extends Component {
    static style = {
        margin: '0 auto',
        maxWidth: '60em',
        width: '100%',
        background: '#f1f1f1',
        padding: '0.5em',
        border: '1px solid #ccc',
        marginTop: '1em'
    };

    static imageRowStyle = {
        margin: '5px 5px 10px',
        padding: '1em'
    };

    static inputStyle = {
        display: 'block'
    };


    constructor(props) {
        super(props);
        this.defaultState = Object.freeze({
            images: {},
            suggestions: [],
            suggestionsLoading: true,
            suggestionsLoadingError: false,
            uploading: false
        });

        this.state = {
            ...this.defaultState
        };
    }

    doSetup() {
        this.setState({
            ...this.defaultState
        });
        fetch('/api/react/tags')
            .then(res => res.json())
            .then((json) => {
                this.setState({suggestions: _map(json.tags, 'name'), suggestionsLoading: false})
            })
            .catch(() => {
                this.setState({suggestionsLoading: false, suggestionsLoadingError: true})
            });
    }

    componentWillMount() {
        this.doSetup();
    }

    autocompleteRenderInput ({alreadyUsedTags}, {addTag, ...props}) {
        const handleOnChange = (e, {newValue, method}) => {
            if (method === 'enter') {
                e.preventDefault()
            } else {
                props.onChange(e)
            }
        };

        const inputValue = (props.value && props.value.trim().toLowerCase()) || '';
        const inputLength = inputValue.length;

        let {suggestions: allSuggestions} = this.state;

        let suggestions = _difference(allSuggestions, alreadyUsedTags).filter((state) => {
            return state.toLowerCase().slice(0, inputLength) === inputValue
        });

        const defaultTheme = {
            container:                'react-autosuggest__container',
            containerOpen:            'react-autosuggest__container--open',
            input:                    'react-autosuggest__input',
            inputOpen:                'react-autosuggest__input--open',
            inputFocused:             'react-autosuggest__input--focused',
            suggestionsContainer:     'react-autosuggest__suggestions-container',
            suggestionsContainerOpen: 'react-autosuggest__suggestions-container--open',
            suggestionsList:          'react-autosuggest__suggestions-list',
            suggestion:               'react-autosuggest__suggestion',
            suggestionFirst:          'react-autosuggest__suggestion--first',
            suggestionHighlighted:    'react-autosuggest__suggestion--highlighted',
            sectionContainer:         'react-autosuggest__section-container',
            sectionContainerFirst:    'react-autosuggest__section-container--first',
            sectionTitle:             'react-autosuggest__section-title'
        };

        const theme = {
            ...defaultTheme,
            suggestion: 'react-tagsinput-tag react-autosuggest__suggestion'
        };

        return (
            <Autosuggest
                theme={theme}
                ref={props.ref}
                suggestions={suggestions}
                shouldRenderSuggestions={(value) => value && value.trim().length > 0}
                getSuggestionValue={(suggestion) => suggestion}
                renderSuggestion={(suggestion) => <span>{suggestion}</span>}
                inputProps={{...props, onChange: handleOnChange}}
                alwaysRenderSuggestions={true}
                onSuggestionSelected={(e, {suggestion}) => {
                    addTag(suggestion)
                }}
                onSuggestionsClearRequested={() => {}}
                onSuggestionsFetchRequested={() => {}}
            />
        )
    }

    onDrop(accepted, rejected) {
        const images = accepted.reduce(function (acc, file) {
            const image = new ReactionImage({
                id: `${file.name}/${file.size}/${+new Date()}`,
                file: file,
                tags: [],
                title: file.name,
                type: file.type
            });
            acc[image.id] = image;
            return acc;
        }, {});
        this.setState({images});
    }

    changeImageValue(id, attribute, event) {
        const images = this.state.images;
        _set(images, [id, attribute], event.target.value);
        this.setState({images});
    }

    changeImageTags(id, tags) {
        const {images, suggestions} = this.state;
        const imageTags = _map(tags, tag => tag.toLowerCase());
        _set(images, [id, 'tags'], imageTags);
        const newSuggestions = _union(suggestions, imageTags);
        this.setState({images, suggestions: newSuggestions});
    }

    uploadImages(event) {
        const {auth} = this.props;
        event.preventDefault();
        const {images} = this.state;
        this.setState({uploading: true});
        const requests = [];
        _forEach(_filter(images, {uploaded: false}), (image, id) => {
            const formData = new FormData();
            formData.append('auth', auth);
            formData.append('file', image.file);
            formData.append('title', image.title);
            formData.append('tags', JSON.stringify(image.tags));
            const req = fetch('/api/react/images', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then((json) => {
                    if (json.ok) {
                        image.uploaded = true;
                        this.setState({images})
                    } else {
                        alert('upload error for ' + id)
                    }
                })
                .catch(() => {
                    image.uploaded = false;
                    image.uploadFailure = true;
                    this.setState({images})
                });
            requests.push(req)
        });
        const setUploadingFalse = () => this.setState({uploading: false});
        Promise.all(requests).then(setUploadingFalse, setUploadingFalse);
    }

    render() {
        const self = NewReactionImageContainer;
        const images = Object.keys(this.state.images).map((image_id) => {
            return this.state.images[image_id];
        });

        const {uploading} = this.state;
        const hasImages = images.length > 0;
        const hasUnuploadedImages = _filter(images, {uploaded: false}).length > 0;
        const textColor = '#2C3E50';
        const bgColor = '#A3B5CB';
        const modal = {
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
        };
        const dropzoneStyles = {
            ...modal,
            width: '100%',
            background: bgColor,
            border: `5px ${textColor} dashed`
        };

        const innerModal = {
            position: 'absolute',
            top: '50%',
            right: '10%',
            left: '10%',
            transform: 'translateY(-50%)',
            textAlign: 'center'
        };

        const dropzoneTextStyles = {
            ...innerModal,
            color: textColor,
        };

        let body = (() => {
            if (hasImages) {
                if (uploading) {
                    return <div style={{...modal, background: '#f1f1f1'}}>
                        <div style={{...innerModal}}>
                            <h1 style={{marginTop: '0'}}>uploading your images<span className="loading">...</span></h1>
                            <div>
                                {images.map((image) => {
                                    return <img src={image.file.preview}
                                                key={image.id}
                                                className={image.uploaded ? '' : 'loading'}
                                                style={{height: images.length > 10 ? '50px' : '100px'}} />
                                })}
                            </div>
                        </div>
                    </div>
                }
                if (!hasUnuploadedImages) {
                    return <div style={{textAlign: 'center', padding: '5px'}}>
                        <h1>Got it! Thanks :^)</h1>
                        <div style={{marginBottom: '1em'}}>
                            <p>
                                <a className="pure-button" href="/react">Image Gallery</a>
                                <span> </span>
                                <button className="pure-button" onClick={this.doSetup.bind(this)}>
                                    <GoCloudUpload /> Upload More Images
                                </button>
                            </p>
                        </div>
                        <div>
                            {images.map((image) => {
                                return <img src={image.file.preview}
                                            key={image.id}
                                            style={{height: images.length > 10 ? '100px' : '150px'}} />
                            })}
                        </div>
                    </div>
                }
                return <form onSubmit={this.uploadImages.bind(this)}>
                    <div className="kiz-upload-menu" style={{background: '#f1f1f1', padding: '5px'}}>
                        <button className="kiz-upload-menu__reset pure-button" onClick={this.doSetup.bind(this)}>
                            <GoChevronLeft/> Select Different Images
                        </button>
                        {hasUnuploadedImages && (
                            <button className="pure-button pure-button-primary"
                                    type="submit"
                                    disabled={this.state.uploading === true}>
                                <GoCloudUpload /> Upload
                            </button>
                        )}
                    </div>
                    {_filter(images, {uploaded: false}).map((image) => {
                        const rowStyle = {
                            ...self.imageRowStyle,
                            background: image.uploaded ? 'white' : '#f1f1f1'
                        };
                        return <div key={image.id} style={rowStyle}>
                            {image.uploaded && <strong>Uploaded successfully</strong>}
                            {image.uploadFailure && <strong style={{color: 'red'}}>This Image Did Not Upload Successfully</strong>}
                            <input type="text"
                                   style={{...self.inputStyle, width: '100%'}}
                                   id="title"
                                   value={image.title}
                                   required={true}
                                   disabled={image.uploaded === true}
                                   onChange={this.changeImageValue.bind(this, image.id, 'title')} />
                            <figure style={{textAlign: 'center'}}>
                                <img src={image.file.preview} style={{maxWidth: '100%'}} />
                            </figure>
                            <div>
                                <TagsInput value={image.tags}
                                           disabled={image.uploaded === true}
                                           renderInput={image.uploaded === true ? undefined : this.autocompleteRenderInput.bind(this, {alreadyUsedTags: image.tags})}
                                           onChange={this.changeImageTags.bind(this, image.id)} />
                            </div>
                        </div>
                    })}
                </form>
            }

            return <div>
                <Dropzone style={dropzoneStyles}
                          className="react-dropzone"
                          accept="image/*"
                          onDrop={this.onDrop.bind(this)}>
                    <div style={dropzoneTextStyles}>
                        <h1 style={{marginTop: '0'}}>please feed me reaction images (✿╹◡╹)</h1>
                        <div style={{position: 'relative'}}>
                            <img src="/static/images/smug.jpg"
                                 style={{maxHeight: '250px', opacity: '0.5'}} />
                            <div style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                width: '5em',
                                height: '5em',
                                transform: 'translate(-50%, -50%)'
                            }}>
                                <GoCloudUpload height="100%" width="100%"/>
                            </div>
                        </div>
                        <strong style={{marginTop: '1em', display: 'block'}}>
                            <button className="pure-button">browse</button> or drag images here.
                        </strong>
                    </div>
                </Dropzone>
            </div>;
        })();


        return <div>
            {body}
        </div>
    }
}