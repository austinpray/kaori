export class ReactionImage {
    constructor({id, description='', file, tags=[], title, type}) {
        this.description = description;
        this.id = id;
        this.file = file;
        this.tags = tags;
        this.title = title;
        this.type = type;
        this.uploaded = false;
    }
}
