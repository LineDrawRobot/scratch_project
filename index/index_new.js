const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const Cast = require('../../util/cast');
const log = require('../../util/log');

const MathUtil = require('../../util/math-util');
const TargetType = require('../../extension-support/target-type');
const Timer = require('../../util/timer')
const fetch = require("node-fetch");
const Scratch3LooksBlocks = require('../../blocks/scratch3_looks');
const Scratch3MotionBlocks = require('../../blocks/scratch3_motion');
const Scratch3PenBlocks = require('../scratch3_pen/index');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/png;base64,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';

//////////////パラメータ//////////////////
var teisoku_kaiten = 36;
var tyusoku_kaiten = 54;
var kousoku_kaiten = 72;
var teisoku_speed = 20;
var tyusoku_speed = 90;
var kousoku_speed = 135;
var vr = 25;
var vl = 50;
var d = 45;//機体サイズ
var correction_time = 3.0;//補正時間
var serial_time = 0.5;//シリアル通信時間
const min_radius = 50; 　　//半径の範囲
const max_radius = 10000;　//半径の範囲

const min_distance = 50; 　　//直進距離の範囲
const max_distance = 20000;　//直進距離の範囲

const min_angle = 1; 　　//角度の範囲
const max_angle = 360;　//角度の範囲

const duration = 1; //シミュレーションの行動１回の動作時間

const raspi = 0; //0:クラウドモード, 1:ラズパイローカルモード

//////////////////////////////////////////


const speed1 = '低速(約' + teisoku_speed + 'cm/s)';
const speed2 = '中速(約' + tyusoku_speed + 'cm/s)';
const speed3 = '高速(約' + kousoku_speed + 'cm/s)';


const rot1 = '低速(約' + teisoku_kaiten + '°/s)';
const rot2 = '中速(約' + tyusoku_kaiten + '°/s)';
const rot3 = '高速(約' + kousoku_kaiten + '°/s)';


var menu_1 = { '前進': 0, '後退': 1 }; //ForB
var menu_2 = { [rot1]: 1, [rot2]: 2, [rot3]: 3 };//SPEED2
var menu_3 = { [speed1]: 1, [speed2]: 2, [speed3]: 3 }; //SPEED
var menu_4 = { '出す': 1, '出さない': 0 }; //INOUT
var menu_5 = { '時計回り': 0, '反時計回り': 1 }; //CW
var menu_6 = { 'シミュレーター': 0, 'ロボット': 1 };//MODE
//var menu_7 = {'中(57°/s・半径67.5cmの円)':2,'小(115°/s・半径45cmの円)':1,'最小':0};//SIZE
var menu_8 = { '10': 10 };
var menu_9 = { '1cm': 1, '10cm': 10, '1m': 100 };
var ptn = { 'A': 1, 'B': 2 }; //ptn
//python対応

const circule_text = '[GRID]に半径[RADIUS]m（' + min_radius / 100 + '~' + max_radius / 100 + '）の円軌道をさせる';

//変数
var mode = 0;
var dx = 0;
var dy = 0;
var degrees = 0;
var jisokuX = 0;
var jisokuY = 0;
var kaiten = 0;
var second = 0;
var grid = 0;
var circleX = 0;
var circleY = 0;
var G = 0;
var p = 0;
var Q = 0;
var inst_n = 0;
var additional_time = 0.0;
var flag = 0;//粉モード0:出さない,1:出す
var flag2 = 0;//粉を出すタイミングを制御
var powdergo = 0;
var powderstop = 0;
var screen_mode = 1;
var content = "";
var looks, pen, motion;
var previous_order = "";
var write_enable = 0;

//信号を送るかの設定はここ使って
function fetch2(text) {
    log.log(text);
    fetch(text);
}

var point = 0;
class Scratch3NewBlocks {
    constructor(runtime) {
        this.runtime = runtime;

        this._counter = 0;
        looks = new Scratch3LooksBlocks(runtime);
        pen = new Scratch3PenBlocks(runtime);
        motion = new Scratch3MotionBlocks(runtime);
        //this.runtime.on('RUNTIME_DISPOSED', this.clearCounter.bind(this));


        this.runtime.on('KEY_PRESSED', key => {
            this.runtime.startHats('event_whenkeypressed', {
                KEY_OPTION: key
            });
            this.runtime.startHats('event_whenkeypressed', {
                KEY_OPTION: 'any'
            });
        });
        //ファイルDL用
        this.downloadLink = document.createElement('a');
        this.downloadLink.setAttribute('href', '#');
        this.downloadLink.setAttribute('download', 'savedata.txt');
    }


    getPrimitives() {
        return {
            motion_movesteps: this.moveSteps,
            motion_gotoxy: this.goToXY,
            motion_goto: this.goTo,
            motion_turnright: this.turnRight,
            motion_turnleft: this.turnLeft,
            motion_pointindirection: this.pointInDirection,
            motion_pointtowards: this.pointTowards,
            motion_glidesecstoxy: this.glide,
            motion_glideto: this.glideTo,
            motion_ifonedgebounce: this.ifOnEdgeBounce,
            motion_setrotationstyle: this.setRotationStyle,
            motion_changexby: this.changeX,
            motion_setx: this.setX,
            motion_changeyby: this.changeY,
            motion_sety: this.setY,
            motion_xposition: this.getX,
            motion_yposition: this.getY,
            motion_direction: this.getDirection,
            // Legacy no-op blocks:
            motion_scroll_right: () => { },
            motion_scroll_up: () => { },
            motion_align_scene: () => { },
            motion_xscroll: () => { },
            motion_yscroll: () => { },
            control_repeat: this.repeat,
            control_repeat_until: this.repeatUntil,
            control_while: this.repeatWhile,
            control_for_each: this.forEach,
            control_forever: this.forever,
            control_wait: this.wait,
            control_wait_until: this.waitUntil,
            control_if: this.if,
            control_if_else: this.ifElse,
            control_stop: this.stop,
            control_create_clone_of: this.createClone,
            control_delete_this_clone: this.deleteClone,
            control_get_counter: this.getCounter,
            control_incr_counter: this.incrCounter,
            control_clear_counter: this.clearCounter,
            control_all_at_once: this.allAtOnce,
            event_whentouchingobject: this.touchingObject,
            event_broadcast: this.broadcast,
            event_broadcastandwait: this.broadcastAndWait,
            event_whengreaterthan: this.hatGreaterThanPredicate
        };
    }




    getMonitored() {
        return {
            motion_xposition: {
                isSpriteSpecific: true,
                getId: targetId => `${targetId}_xposition`
            },
            motion_yposition: {
                isSpriteSpecific: true,
                getId: targetId => `${targetId}_yposition`
            },
            motion_direction: {
                isSpriteSpecific: true,
                getId: targetId => `${targetId}_direction`
            }
        };
    }

    getInfo() {
        return {
            id: 'newblocks',
            name: 'ライン引き',
            blockIconURI: blockIconURI,
            blocks: [
                {
                    opcode: 'fetchURL16',
                    blockType: BlockType.HAT,
                    text: 'プログラム開始',
                    arguments: {
                        defaultValue: false
                    },
                    isEdgeActivated: false
                },
                {
                    opcode: 'fetchURL1',
                    blockType: BlockType.COMMAND,
                    text: '[TEXT]を起動',
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "シミュレーター",
                            menu: 'MENU6'
                        }
                    }
                },
                {
                    opcode: 'fetchURL2',
                    blockType: BlockType.COMMAND,
                    text: 'プログラム終了'
                },                
                {
                    opcode: 'fetchURL4',
                    blockType: BlockType.COMMAND,
                    text: 'タイヤを止める',
                },
                {
                    opcode: 'fetchURL5',
                    blockType: BlockType.COMMAND,
                    text: '粉を[TEXT]',
                    arguments: {
                        TEXT: {
                            type: ArgumentType.STRING,
                            defaultValue: "出す",
                            menu: 'MENU4'
                        }
                    },
                    filter: [TargetType.SPRITE]
                },/*
                {
                    opcode: 'fetchURL3',
                    blockType: BlockType.COMMAND,
                    text: '[TEXT3]で[TEXT2]させる',
                    arguments: {
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: "前進",
                            menu: 'MENU1'
                        },
                        TEXT3: {
                            type: ArgumentType.STRING,
                            defaultValue: speed1,
                            menu: "MENU3"
                        }
                    }
                },
                {
                    opcode: 'fetchURL6',
                    blockType: BlockType.COMMAND,
                    text: '[TEXT1]に[TEXT2]で旋回させる',
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: "時計回り",
                            menu: 'MENU5'
                        },
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: rot1,
                            menu: 'MENU2'
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {

                    opcode: 'fetchURL19',
                    blockType: BlockType.COMMAND,
                    text: '[GRID]に半径[RADIUS]m（範囲：' + min_radius / 100 + '~' + max_radius / 100 + '）の円軌道をさせる',
                    arguments: {
                        GRID: {
                            type: ArgumentType.STRING,
                            defaultValue: "時計回り",
                            menu: 'MENU5'

                        },
                        RADIUS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        }
                    }

                },*/
                {
                    opcode: 'fetchURL3_2',
                    blockType: BlockType.COMMAND,
                    text: '[TEXT1]m（範囲：' + min_distance / 100 + '~' + max_distance / 100 + '）[TEXT2]させる',
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        },
                        TEXT2: {
                            type: ArgumentType.STRING,
                            defaultValue: "前進",
                            menu: 'MENU1'
                        }
                    }
                },
                {
                    opcode: 'fetchURL6_2',
                    blockType: BlockType.COMMAND,
                    text: '[TEXT1]に[TEXT2]度（範囲：' + min_angle + '~' + max_angle + '）[旋回させる',
                    arguments: {
                        TEXT1: {
                            type: ArgumentType.STRING,
                            defaultValue: "時計回り",
                            menu: 'MENU5'
                        },
                        TEXT2: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        }
                    },
                    filter: [TargetType.SPRITE]
                },
                {

                    opcode: 'fetchURL19_2',
                    blockType: BlockType.COMMAND,
                    text: '[GRID]に半径[RADIUS]m（範囲：' + min_radius / 100 + '~' + max_radius / 100 + '）の円軌道を[ANGLE]度（範囲：' + min_angle + '~' + max_angle + '）させる',
                    arguments: {
                        GRID: {
                            type: ArgumentType.STRING,
                            defaultValue: "時計回り",
                            menu: 'MENU5'

                        },
                        RADIUS: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        },
                        ANGLE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        }

                    }

                },
                {
                    opcode: 'fetchURL7',
                    blockType: BlockType.LOOP,
                    text: '[TIMES]回繰り返す',
                    arguments: {
                        TIMES: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        }
                    },
                    isEdgeActivated: true
                },


                {
                    opcode: 'fetchURL11',
                    blockType: BlockType.COMMAND,
                    text: '[EXECUTE]秒動かす',
                    arguments: {
                        EXECUTE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "1"
                        }
                    }
                },
                /*
                {
                    opcode:'fetchURL14',
                    blockType:BlockType.COMMAND,
                    text:'[GRID]で[CIRCLE]回転させる',
                    arguments:{
                        GRID:{
                            type:ArgumentType.STRING,
                            defaultValue:"時計回り",
                            menu:'MENU5'
                        },
                        CIRCLE:{
                            type:ArgumentType.STRING,
                            defaultValue:"中(57°/s・半径67.5cmの円)",
                            menu:'MENU7'
                        }
                    }   
                },
                */


                {
                    opcode: 'clear',
                    blockType: BlockType.COMMAND,
                    text: 'シミュレーターの線を消す'
                },

                {
                    opcode: 'fetchURL18',
                    blockType: BlockType.COMMAND,
                    text: 'x座標を[setX]、y座標を[setY]、向きを[setTurn]にする',
                    arguments: {
                        setX: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0"
                        },
                        setY: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "0"
                        },
                        setTurn: {
                            type: ArgumentType.NUMBER,
                            defaultValue: "90"
                        }
                    },
                },


                {
                    opcode: 'fetchURL20',
                    blockType: BlockType.COMMAND,
                    text: '座標のサイズを[SIZE]単位とする',
                    arguments: {
                        SIZE: {
                            type: ArgumentType.STRING,
                            defaultValue: "1cm",
                            menu: 'MENU8'

                        }
                    }

                },

                /*
                {
                 opcode: 'writeFile',
                 text: 'プログラムのダウンロード',
                 blockType: BlockType.COMMAND,
                },*/
                {
                    opcode: 'fetchURL21',
                    blockType: BlockType.COMMAND,
                    text: '命令を送信（クラウド用パスワード：[PASS]）',
                    arguments: {
                        PASS: {
                            type: ArgumentType.STRING,
                            defaultValue: "　　　　　"
                        }
                    }


                }


            ],
            menus: {
                MENU1: { //ForB
                    items: ['前進', '後退']
                },
                MENU2: { //SPEED2
                    items: [rot1/*,rot2,rot3*/]
                },
                MENU3: { //SPEED
                    items: [speed1/*, speed2, speed3*/]
                },
                MENU4: { //INOUT
                    items: ['出す', '出さない']
                },
                MENU5: { //CW
                    items: ['時計回り', '反時計回り']
                },
                MENU6: { //MODE
                    items: ['シミュレーター', 'ロボット']
                },
                MENU7: { //SIZE
                    items: ['中(57°/s・半径67.5cmの円)', '小(115°/s・半径45cmの円)', '最小']
                },
                MENU8: { //
                    items: ['1cm', '10cm', '1m']
                }
            }
        };
    }

    fetchURL1(args, util)//全体起動
    {
        if (write_enable == 1) {

            if (menu_6[Cast.toString(args.TEXT)] == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=START";
                const text = server + inst;
                mode = menu_6[Cast.toString(args.TEXT)];
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                previous_order = inst;
            }
            else {
                const text = "start";
                mode = menu_6[Cast.toString(args.TEXT)];
                looks.say({ mutation: undefined, MESSAGE: '' }, util);
                log.log("起動");
            }
        }
    }

    fetchURL2(args, util)//全体停止
    {
        if (write_enable == 1) {
            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=STOP";
                const text = server + inst;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                previous_order = inst;
                looks.say({ mutation: undefined, MESSAGE: '命令セット完了' }, util);
            }
            else {
                log.log("停止")
                util.stopAll();

            }
            write_enable = 2;
        }
    }

    fetchURL3(args, util)//移動
    {
        if (write_enable == 1) {
            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=TIREON";
                const text2 = "&ForB=" + menu_1[Cast.toString(args.TEXT2)];
                const text3 = "&SPEED=" + menu_3[Cast.toString(args.TEXT3)];
                const text = server + inst + text2 + text3;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                const current_order = inst + text2 + text3;
                if (current_order != previous_order) additional_time = correction_time;//ステアリング補正時間
                else additional_time = 0.0;
                previous_order = inst + text2 + text3;
                flag2 = 1;
            }
            else {
                const radians = MathUtil.degToRad(90 - util.target.direction);
                point = 0;
                if (menu_3[Cast.toString(args.TEXT3)] == 1) //低速
                {
                    dx = teisoku_speed * Math.cos(radians) / screen_mode;
                    dy = teisoku_speed * Math.sin(radians) / screen_mode;;
                }
                else if (menu_3[Cast.toString(args.TEXT3)] == 2) //中速
                {
                    dx = tyusoku_speed * Math.cos(radians) / screen_mode;;
                    dy = tyusoku_speed * Math.sin(radians) / screen_mode;;
                }
                else//                            //高速
                {
                    dx = kousoku_speed * Math.cos(radians) / screen_mode;;
                    dy = kousoku_speed * Math.sin(radians) / screen_mode;;
                }

                //log.log('dx','dy',dx,dy);

                if (menu_1[Cast.toString(args.TEXT2)] == 0)//前
                {
                    jisokuX = dx;
                    jisokuY = dy;
                }

                else if (menu_1[Cast.toString(args.TEXT2)] == 1) {
                    jisokuX = -dx;
                    jisokuY = -dy;
                }
            }
            log.log("前後移動");
        }
    }
    fetchURL3_2(args, util)//移動
    {
        if (write_enable == 1) {

            var num = Math.floor(Cast.toNumber(args.TEXT1) * 100);
            if (num < min_distance) num = min_distance;
            else if (num > max_distance) num = max_distance;
            else num = num;

            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=TIREON";              
                const text1 = "&DISTANCE=" + num;
                const text2 = "&ForB=" + menu_1[Cast.toString(args.TEXT2)];
                const text = server + inst + text1 + text2;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                const current_order = inst + text1 + text2;
                if (current_order != previous_order) additional_time = correction_time;//ステアリング補正時間
                else additional_time = 0.0;
                previous_order = inst + text1 + text2;
                flag2 = 1;
            }
            else {
                const radians = MathUtil.degToRad(90 - util.target.direction);
                point = 0;
                dx = num * Math.cos(radians) / screen_mode;
                dy = num * Math.sin(radians) / screen_mode;
                
                if (menu_1[Cast.toString(args.TEXT2)] == 0)//前
                {
                    jisokuX = util.target.x + dx;
                    jisokuY = util.target.y + dy;
                }

                else if (menu_1[Cast.toString(args.TEXT2)] == 1) {
                    jisokuX = util.target.x - dx;
                    jisokuY = util.target.y - dy;
                }
                log.log(jisokuX);
                log.log(jisokuY);
                motion.glide ({ mutation: undefined, SECS: '1', X: String(jisokuX), Y: String(jisokuY)}, util) 

                
            }
            log.log("前後移動");
        }
    }

    fetchURL4(args, util) //動作の停止
    {
        if (write_enable == 1) {
            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=TIREOFF";
                const text1 = "&SPEED=STOP";
                const text = server + inst + text1;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                //previous_order=inst+text1;
            }
            else {
                point = 1;
                kaiten = 0;
                log.log("タイヤ停止");
            }
        }
    }

    fetchURL5(args, util)//粉
    {
        if (write_enable == 1) {
            if (mode == 1) {

                if (menu_4[Cast.toString(args.TEXT)] == 1) {
                    flag = 1;
                }
                else {
                    flag = 0;

                }
            }
            else {
                if (menu_4[Cast.toString(args.TEXT)] == 1)//出す
                {

                    pen.setPenSizeTo({ mutation: undefined, SIZE: '5' }, util);
                    pen.setPenColorParamTo({ mutation: undefined, COLOR_PARAM: 'color', VALUE: '0' }, util);
                    pen.setPenColorParamTo({ mutation: undefined, COLOR_PARAM: 'saturation', VALUE: '0' }, util);
                    pen.setPenColorParamTo({ mutation: undefined, COLOR_PARAM: 'brightness', VALUE: '100' }, util);
                    pen.penDown(args, util);

                }
                else //出さない
                {
                    pen.penUp(args, util)
                }
            }
            log.log("粉");
        }
    }


    fetchURL6(args, util)//回転
    {
        if (write_enable == 1) {
            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=TURN";
                const text1 = "&CW=" + menu_5[Cast.toString(args.TEXT1)];
                const text2 = "&SPEED=" + menu_2[Cast.toString(args.TEXT2)];
                const text = server + inst + text1 + text2;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                previous_order = inst + text1 + text2;
                //ステアリング補正時間
                additional_time = correction_time;
            }

            else {

                point = 1;
                if (menu_2[Cast.toString(args.TEXT2)] == 1)//低速
                {
                    const W = Cast.toNumber(teisoku_speed * 2 / d);
                    degrees = Math.abs(((180 * (W) / (Math.PI))).toFixed());
                    degrees = teisoku_kaiten;
                }
                else if (menu_2[Cast.toString(args.TEXT2)] == 2)//中速
                {
                    const W = Cast.toNumber(tyusoku_speed * 2 / d);
                    degrees = Math.abs(((180 * (W) / (Math.PI))).toFixed());
                    degrees = tyusoku_kaiten;
                }
                else {
                    const W = Cast.toNumber(kousoku_speed * 2 / d);//高速
                    degrees = Math.abs(((180 * (W) / (Math.PI))).toFixed());
                    degrees = kousoku_kaiten;
                }

                if (menu_5[Cast.toString(args.TEXT1)] == 0)//時計回り
                {

                    kaiten = degrees;
                    log.log('degrees', degrees);
                }

                else //if(menu_5[Cast.toString(args.TEXT1)] == 1)//反時計回り
                {
                    kaiten = -degrees;
                    log.log('degrees', degrees);
                }
            }
        }
    }
    fetchURL6_2(args, util)//回転
    {
        if (write_enable == 1) {
            
            var num = Math.floor(Cast.toNumber(args.TEXT2));
            if (num < min_angle) num = min_angle;
            else if (num > max_angle) num = max_angle;
            else num = num;

            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=TURN";
                const text1 = "&CW=" + menu_5[Cast.toString(args.TEXT1)];
                const text2 = "&ANGLE=" + num;
                const text = server + inst + text1 + text2;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
                previous_order = inst + text1 + text2;
                //ステアリング補正時間
                additional_time = correction_time;
            }

            else {

                point = 1;
                
                if (menu_5[Cast.toString(args.TEXT1)] == 0)//時計回り
                {

                    motion.turnRight({ mutation: undefined, DEGREES: String(num)}, util);
                }

                else //反時計回り
                {
                    motion.turnLeft({ mutation: undefined, DEGREES: String(num)}, util);
                }
            }
        }
    }
    fetchURL7(args, util) //;繰り返す
    {
        const times = Math.round(Cast.toNumber(args.TIMES));
        // Initialize loop
        if (typeof util.stackFrame.loopCounter === 'undefined') {
            util.stackFrame.loopCounter = times;
        }
        // Only execute once per frame.
        // When the branch finishes, `repeat` will be executed again and
        // the second branch will be taken, yielding for the rest of the frame.
        // Decrease counter
        util.stackFrame.loopCounter--;
        // If we still have some left, start the branch.
        if (util.stackFrame.loopCounter >= 0) {
            util.startBranch(1, true);
        }
    }

    clear() //線を消す
    {

        pen.clear()
    }

    fetchURL11(args, util) {//●秒動かす
        if (write_enable == 1) {
            if (mode == 1) {
                const server = "http://localhost:8000?";
                if (flag == 1 && flag2 == 1) { //flag →粉を出すか  flag2 →　直進か円軌道か
                    var inst = "inst_n=" + (inst_n++) + "&inst=SLEEP";
                    var text1 = "&TIME=" + additional_time;
                    var text = server + inst + text1;
                    if (raspi == 1) fetch2(text);
                    content = content + text + '\n';

                    inst = "inst_n=" + (inst_n++) + "&inst=POWDER";//大文字
                    text1 = "&INOUT=" + 1;
                    text = server + inst + text1;
                    if (raspi == 1) fetch2(text);
                    content = content + text + '\n';

                    inst = "inst_n=" + (inst_n++) + "&inst=SLEEP";
                    text1 = "&TIME=" + Cast.toNumber(args.EXECUTE);
                    text = server + inst + text1;
                    if (raspi == 1) fetch2(text);
                    content = content + text + '\n';

                    flag2 = 0;
                    inst = "inst_n=" + (inst_n++) + "&inst=POWDER";//大文字
                    text1 = "&INOUT=" + 0;
                    text = server + inst + text1;
                    if (raspi == 1) fetch2(text);
                    content = content + text + '\n';
                    additional_time = 0.0;
                } else {
                    var inst = "inst_n=" + (inst_n++) + "&inst=SLEEP";
                    var text1 = "&TIME=" + (additional_time + Cast.toNumber(args.EXECUTE));
                    var text = server + inst + text1;
                    if (raspi == 1) fetch2(text);
                    content = content + text + '\n';
                    flag2 = 0;
                }


            }
            else {
                //if (util.stackFrame.timer) { //新たにタイマーを動かしたとき        
                //  var timeElapsed = util.stackFrame.timer.timeElapsed(); //新たなタイマーを動かしてからの経過時間

                switch (point) {
                    case 0:
                        if (util.stackFrame.timer) {
                            const timeElapsed = util.stackFrame.timer.timeElapsed();
                            if (timeElapsed < util.stackFrame.duration * 1000) {

                                const frac = timeElapsed / (util.stackFrame.duration * 1000);
                                const dx = frac * (util.stackFrame.endX);
                                const dy = frac * (util.stackFrame.endY);
                                util.target.setXY(
                                    util.stackFrame.startX + dx,
                                    util.stackFrame.startY + dy
                                );
                                util.yield();
                            }
                            else {
                                // 最後の移動
                                util.target.setXY(util.stackFrame.startX + util.stackFrame.endX, util.stackFrame.startY + util.stackFrame.endY);
                            }
                        } else {
                            util.stackFrame.timer = new Timer();
                            util.stackFrame.timer.start();
                            util.stackFrame.duration = duration;
                            util.stackFrame.startX = util.target.x;
                            util.stackFrame.startY = util.target.y;
                            util.stackFrame.endX = Cast.toNumber(args.EXECUTE) * jisokuX;
                            util.stackFrame.endY = Cast.toNumber(args.EXECUTE) * jisokuY;
                            if (util.stackFrame.duration <= 0) {
                                // 動作時間が0秒の場合
                                log.log("動作時間が不正です")
                                return;
                            }
                            util.yield();
                        }
                        break;
                    case 1:
                        if (util.stackFrame.timer) {
                            const timeElapsed = util.stackFrame.timer.timeElapsed();
                            if (timeElapsed < util.stackFrame.duration * 1000) {
                                const frac = timeElapsed / (util.stackFrame.duration * 1000);
                                const dr = frac * util.stackFrame.endR;
                                util.target.setDirection(util.stackFrame.startR + dr);
                                util.yield();
                            } else {
                                // 最後の回転
                                util.target.setDirection(util.stackFrame.startR + util.stackFrame.endR);

                            }
                        } else {
                            util.stackFrame.timer = new Timer();
                            util.stackFrame.timer.start();
                            util.stackFrame.duration = duration;
                            util.stackFrame.startR = util.target.direction;
                            util.stackFrame.endR = Cast.toNumber(args.EXECUTE) * kaiten;

                            if (util.stackFrame.duration <= 0) {
                                // 動作時間が0秒の場合
                                log.log("動作時間が不正です")
                                return;
                            }
                            util.yield();
                        }
                        break;


                    case 2:

                        if (util.stackFrame.timer) {
                            const timeElapsed = util.stackFrame.timer.timeElapsed();
                            if (timeElapsed < util.stackFrame.duration * 1000) {
                                const frac = timeElapsed / (util.stackFrame.duration * 1000);

                                const t_m = (util.stackFrame.endR) * frac;
                                util.target.setDirection(util.stackFrame.startR + t_m);
                                const tmp_r = util.stackFrame.startR + t_m;
                                const dx = G * ((p * Math.cos((Math.PI * (tmp_r)) / 180)) * -1);　//移動量X
                                const dy = G * (p * Math.sin((Math.PI * (tmp_r)) / 180));　//移動量Y
                                util.target.setXY(circleX + dx, circleY + dy);
                                util.yield();
                            }
                            else {
                                // 最後の移動
                                util.target.setXY(circleX + util.stackFrame.endX, circleY + util.stackFrame.endY);
                                util.target.setDirection(util.stackFrame.startR + util.stackFrame.endR);

                                point = 0;

                            }
                        }
                        else {
                            // First time: save data for future use.
                            util.stackFrame.timer = new Timer();
                            util.stackFrame.timer.start();
                            util.stackFrame.duration = duration;
                            util.stackFrame.startX = util.target.x;
                            util.stackFrame.startY = util.target.y;
                            util.stackFrame.startR = util.target.direction;
                            const Grid = util.stackFrame.startR + (Cast.toNumber(args.EXECUTE) * grid) * G;
                            util.stackFrame.endX = G * ((p * Math.cos((Math.PI * (Grid)) / 180)) * -1);
                            util.stackFrame.endY = G * (p * Math.sin((Math.PI * (Grid)) / 180));
                            util.stackFrame.endR = (Cast.toNumber(args.EXECUTE) * grid) * G;
                            if (util.stackFrame.duration <= 0) {
                                // 動作時間が0秒の場合
                                log.log("動作時間が不正です")
                                return;
                            }
                            util.yield();
                        }

                        break;

                }
            }
        }
    }


    /*
    fetchURL14(args,util)//size,CW,ptn
    {
        if( tyusoku_speed / teisoku_speed >= kousoku_speed / tyusoku_speed ){
            ptn = 1;
        }
        
        else{
            ptn = 2;
        }
        
        if ( mode == 1 ){
            const server="http://localhost:8000?";
            const inst = "inst=CIRCLE"; 
            const text2 = "&SIZE="+menu_7[Cast.toString(args.CIRCLE)];
            const text = "&CW="+menu_5[Cast.toString(args.GRID)];
            const text3 = "&ptn="+ptn;
            const text0= server+inst+text+text2;//+text3;
            if(raspi==1) fetch2(text0);
            content=content+inst+text+text2+text3+'\n';
     
            //ステアリング補正時間
            additional_time=correction_time;
            flag2=1;
        }
        
        else{
            if(menu_5[Cast.toString(args.GRID)] == 0)//時計回り
            {
                G = 1;
                if(menu_7[Cast.toString(args.CIRCLE)] == 1)//小さい
                {
                    vr = teisoku_speed;
                    vl = kousoku_speed;
                }
                
                else if(ptn == 1)//　中/低 >= 高/中
                {
                    
                    if(menu_7[Cast.toString(args.CIRCLE)] == 2)//中くらい
                    {
                        vr = teisoku_speed;
                        vl = tyusoku_speed;
                    }
                    
                    else if(menu_7[Cast.toString(args.CIRCLE)] == 3)//大きい
                    {
                        vr = tyusoku_speed;
                        vl = kousoku_speed;
                    }
                }
                
                else if(ptn == 2)//　高/中 > 中/低
                {
                    if(menu_7[Cast.toString(args.CIRCLE)] == 2)//中くらい
                    {
                        vr = tyusoku_speed;
                        vl = kousoku_speed;
                    }
                    
                    else if(menu_7[Cast.toString(args.CIRCLE)] == 3)//大きい
                    {
                        vr = teisoku_speed;
                        vl = tyusoku_speed;
                    }
                }
            }
            else if(menu_5[Cast.toString(args.GRID)] == 1)//反時計回り
            {
                G = -1;
                if(menu_7[Cast.toString(args.CIRCLE)] == 1)//小さい
                {
                    vr = kousoku_speed;
                    vl = teisoku_speed;
                }
                
                else if(ptn == 1)//　中/低 >= 大/中
                {
                    
                    if(menu_7[Cast.toString(args.CIRCLE)] == 2)//中くらい
                    {
                        vl = teisoku_speed;
                        vr = tyusoku_speed;
                    }
                    
                    else if(menu_7[Cast.toString(args.CIRCLE)] == 3)//大きい
                    {
                        vl = tyusoku_speed;
                        vr = kousoku_speed;
                    }
                }
                
                else if(ptn == 2)//　高/中 > 中/低
                {
                    if(menu_7[Cast.toString(args.CIRCLE)] == 2)//中くらい
                    {
                        vl = tyusoku_speed;
                        vr = kousoku_speed;
                    }
                    
                    else if(menu_7[Cast.toString(args.CIRCLE)] == 3)//大きい
                    {
                        vl = teisoku_speed;
                        vr = tyusoku_speed;
                    }
                }
            }
     
        const V1 = vr-vl;
        const V2 = vr+vl;
        const d = 45;
     
        grid = Math.abs((360 * (V1/d)/(2*Math.PI)).toFixed()) ;//角速度
     
        const V3 = V2/V1;
        p = Math.abs((d/2) * V3) ;//半径
    log.log("円:",grid, V3, p);
        circleX = util.target.x + (G * (p*(Math.cos(Math.PI * (Cast.toNumber(util.target.direction)) / 180).toFixed(10)))) ;
        circleY = util.target.y + ( G *(-1* (p *(Math.sin(Math.PI * (Cast.toNumber(util.target.direction)) / 180).toFixed(10)))));
        log.log("円2:",circleX,circleY);
        point = 2;
        
        }
     
    }*/
    /**
        fetchURL15 (args,util) { //wait
            if (util.stackTimerNeedsInit()) {
                const duration = Math.max(0, 1000);
     
                util.startStackTimer(duration);
                this.runtime.requestRedraw();
                util.yield();
            } else if (!util.stackTimerFinished()) {
                util.yield();
            }
        }
    **/
    fetchURL16(args, util) {
        mode = 0;
        dx = 0;
        dy = 0;
        degrees = 0;
        jisokuX = 0;
        jisokuY = 0;
        kaiten = 0;
        second = 0;
        grid = 0;
        circleX = 0;
        circleY = 0;
        G = 0;
        p = 0;
        Q = 0;
        additional_time = 0.0;
        inst_n = 0;
        flag = 0;
        flag2 = 0;
        write_enable = 1;
        content = "instruction\n";
        const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
        const inst = "&inst=RESET";
        const text = server + inst;
        if (raspi == 1 && mode == 1) fetch2(text);

        previous_order = inst;
        looks.say({ mutation: undefined, MESSAGE: '' }, util);
        return {
            event_whenflagclicked: {
                restartExistingThreads: true
            }
        };


    }


    fetchURL18(args, util) //初期位置
    {
        const x = Cast.toNumber(args.setX);
        const y = Cast.toNumber(args.setY);
        const degrees = Cast.toNumber(args.setTurn);
        util.target.setXY(x, y);
        util.target.setDirection(degrees);
    }




    fetchURL19(args, util)//半径指定の円軌道
    {
        if (write_enable == 1) {
            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=CIRCLE3";
                const text1 = "&CW=" + menu_5[Cast.toString(args.GRID)];
                var num = Math.floor(Cast.toNumber(args.RADIUS) * 100);

                if (num < min_radius) num = min_radius;
                else if (num > max_radius) num = max_radius;
                else num = num;

                const text2 = "&turnsize=" + num;//+Cast.toNumber(args.RADIUS)*100;
                const text = server + inst + text1 + text2;
                const current_order = inst + text1 + text2;
                if (current_order != previous_order) additional_time = correction_time;//ステアリング補正時間
                else additional_time = 0.0;
                previous_order = inst + text1 + text2;

                flag2 = 1;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
            }
            else {

                if (menu_5[Cast.toString(args.GRID)] == 0) G = 1; //時計回り     
                else G = -1; //反時計回り  

                var p1 = Math.floor(Cast.toNumber(args.RADIUS) * 100);

                if (p1 < min_radius) p1 = min_radius;
                else if (p1 > max_radius) p1 = max_radius;
                else p1 = p1;


                p = p1 / screen_mode;//半径
                grid = Math.abs((360 * (100 / p1) / (2 * Math.PI)));//角速度

                log.log("円:", grid, p);
                circleX = util.target.x + (G * (p * (Math.cos(Math.PI * (Cast.toNumber(util.target.direction)) / 180).toFixed(10))));//中心点x
                circleY = util.target.y + (G * (-1 * (p * (Math.sin(Math.PI * (Cast.toNumber(util.target.direction)) / 180).toFixed(10)))));//中心点y
                log.log("円2:", circleX, circleY);
                point = 2;
            }
        }
    }
    fetchURL19_2(args, util)//半径指定の円軌道
    {
        if (write_enable == 1) {
            var num = Math.floor(Cast.toNumber(args.RADIUS) * 100);
            if (num < min_radius) num = min_radius;
            else if (num > max_radius) num = max_radius;
            else num = num;
            var num2 = Math.floor(Cast.toNumber(args.ANGLE));
            if (num2 < min_angle) num = min_angle;
            else if (num2 > max_angle) num = max_angle;
            else num2 = num2;


            if (mode == 1) {
                const server = "http://localhost:8000?" + "inst_n=" + (inst_n++);
                const inst = "&inst=CIRCLE3";
                const text1 = "&CW=" + menu_5[Cast.toString(args.GRID)];
                const text2 = "&turnsize=" + num;//+Cast.toNumber(args.RADIUS)*100;
                const text3 = "&ANGLE=" + num2;
                const text = server + inst + text1 + text2 + text3;
                const current_order = inst + text1 + text2 + text3;
                if (current_order != previous_order) additional_time = correction_time;//ステアリング補正時間
                else additional_time = 0.0;
                previous_order = inst + text1 + text2 + text3;
                flag2 = 1;
                if (raspi == 1) fetch2(text);
                content = content + text + '\n';
            }
            else {

                if (menu_5[Cast.toString(args.GRID)] == 0) G = 1; //時計回り     
                else G = -1; //反時計回り  

                var p1 = Math.floor(Cast.toNumber(args.RADIUS) * 100);

                if (p1 < min_radius) p1 = min_radius;
                else if (p1 > max_radius) p1 = max_radius;
                else p1 = p1;


                p = p1 / screen_mode;//半径
                grid = Math.abs((360 * (100 / p1) / (2 * Math.PI)));//角速度

                log.log("円:", grid, p);
                circleX = util.target.x + (G * (p * (Math.cos(Math.PI * (Cast.toNumber(util.target.direction)) / 180).toFixed(10))));//中心点x
                circleY = util.target.y + (G * (-1 * (p * (Math.sin(Math.PI * (Cast.toNumber(util.target.direction)) / 180).toFixed(10)))));//中心点y
                log.log("円2:", circleX, circleY);
                point = 2;
            }
        }
    }
    fetchURL20(args, util) //画面サイズ変更
    {
        const size = menu_9[Cast.toString(args.SIZE)];
        log.log("円2:", size);
        screen_mode = size;
        if (size == 1) util.target.setSize(100);
        else if (size == 10) util.target.setSize(60);
        else util.target.setSize(30);




    }


    fetchURL21(args, util) {
        if (mode == 1 && write_enable == 2) {
            write_enable = 0;

            if (raspi == 1) {
                const server = "http://localhost:8000?";
                const inst = "inst_n=" + (inst_n++) + "&inst=EXECUTE";
                const text0 = server + inst;
                fetch2(text0);
            } else {

                const url = 'https://hooks.slack.com/services/' + args.PASS; // TODO: set WebhookURL
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json'
                    },
                    //body: JSON.stringify({ text: Cast.toString(args.WORD) })
                    body: JSON.stringify({ text: content })
                }).then(response => console.log)
                    .catch(error => alert('error!!'));
                content = "";
            }
            looks.sayforsecs({ mutation: undefined, MESSAGE: '命令実行', SECS: '5' }, util);
        }
    }

    writeFile() {
        this.downloadCallback = () => {
            const blob = new Blob([content], { "type": "text/plain" });
            if (window.navigator.msSaveBlob) {
                window.navigator.msSaveBlob(blob, "test.txt");
            } else {
                this.downloadLink.href = window.URL.createObjectURL(blob);
            }
        };

        this.downloadLink.addEventListener('click', this.downloadCallback);
        this.downloadLink.click();
        this.downloadLink.removeEventListener('click', this.downloadCallback);
    }


}







module.exports = Scratch3NewBlocks;
