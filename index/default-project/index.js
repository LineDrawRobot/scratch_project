import projectData from './project-data';

/* eslint-disable import/no-unresolved */
import popWav from '!arraybuffer-loader!./83a9787d4cb6f3b7632b4ddfebf74367.wav?';
import meowWav from '!arraybuffer-loader!./83c36d806dc92327b9e7049a565c6bff.wav?';
import backdrop from '!raw-loader!./cd21514d0531fdffb22204e0ec5ed84a.svg?';
import costume1 from '!raw-loader!./bcf454acf82e4504149f7ffe07081dbc.svg?';
import costume2 from '!raw-loader!./0fb9be3e8397c983338cb71dc84d0b25.svg?';

// 👇 【追加】新しいアセット（背景のSVGと、新しいスプライトのPNG）をインポート
import newBackdrop from '!raw-loader!./5978c66a8a972c2b6f6e191a21601468.svg?';
import iconScratchPng from '!arraybuffer-loader!./ffef3feb8fa5045f499371ab6fc58730.png?';
////////////////////////////////////////////////////////////////////////////

/* eslint-enable import/no-unresolved */

const defaultProject = translator => {
    let _TextEncoder;
    if (typeof TextEncoder === 'undefined') {
        _TextEncoder = require('fastestsmallesttextencoderdecoder').TextEncoder;
    } else {
        _TextEncoder = TextEncoder;
    }
    const encoder = new _TextEncoder();

    const projectJson = projectData(translator);
    return [{
        id: 0,
        assetType: 'Project',
        dataFormat: 'JSON',
        data: JSON.stringify(projectJson)
    }, {
        id: '83a9787d4cb6f3b7632b4ddfebf74367',
        assetType: 'Sound',
        dataFormat: 'WAV',
        data: new Uint8Array(popWav)
    }, {
        id: '83c36d806dc92327b9e7049a565c6bff',
        assetType: 'Sound',
        dataFormat: 'WAV',
        data: new Uint8Array(meowWav)
    }, {
        id: 'cd21514d0531fdffb22204e0ec5ed84a',
        assetType: 'ImageVector',
        dataFormat: 'SVG',
        data: encoder.encode(backdrop)
    }, {
        id: 'bcf454acf82e4504149f7ffe07081dbc',
        assetType: 'ImageVector',
        dataFormat: 'SVG',
        data: encoder.encode(costume1)
    }, {
        id: '0fb9be3e8397c983338cb71dc84d0b25',
        assetType: 'ImageVector',
        dataFormat: 'SVG',
        data: encoder.encode(costume2)
    }, {
        // 👇 【追加】新しい背景（SVG）のデータ登録
        id: '5978c66a8a972c2b6f6e191a21601468',
        assetType: 'ImageVector',
        dataFormat: 'SVG',
        data: encoder.encode(newBackdrop)
    }, {
        // 👇 【追加】新しいスプライト（PNG）のデータ登録
        id: 'ffef3feb8fa5045f499371ab6fc58730',
        assetType: 'ImageBitmap',
        dataFormat: 'PNG',
        data: new Uint8Array(iconScratchPng)
    }];
};

export default defaultProject;