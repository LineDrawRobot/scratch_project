/*
Issue #11
ステアリング角制御の関数化に伴うバグの改善
*/

#include <SparkFun_BNO08x_Arduino_Library.h>
#include <Wire.h>
#include <stdint.h>
#include <math.h>
#include <LiquidCrystal_I2C.h>
#include <serial_spi.h>

// IMU用インスタンス
BNO08x myIMU;

// IMUの設定
#define BNO08X_ADDR 0x4B  // SparkFun BNO08x Breakout (Qwiic) defaults to 0x4B
#define BNO08X_INT -1
#define BNO08X_RST -1

// タイマー設定
#define TC 15

// 制御信号読み取りピン(RaspberryPi側からの信号)
#define SERVO_ON 22
#define POWDER_DROP 23
#define RIGHT_WHEEL_DIRECTION 24
#define LEFT_WHEEL_DIRECTION 25
#define RIGHT_WHEEL_SPEED_U 26
#define RIGHT_WHEEL_SPEED_D 27
#define LEFT_WHEEL_SPEED_U 28
#define LEFT_WHEEL_SPEED_D 29

/*------------------モータ系の設定---------------------*/
// モータ速度設定
#define WHEEL_STOP 128         // モータが停止する値
#define WHEEL_SPEED_STEP_R 25  // 3段階の速度1段分の速度変化
#define WHEEL_SPEED_STEP_L 25
#define WHEEL_SPEED_STEP_ROT 20  //旋回ベース速度

// モータ制御用ピン
#define PWM_PIN1 4
#define PWM_PIN2 5
#define MOTOR_DRIVE_PIN1 2
#define MOTOR_DRIVE_PIN2 3
#define DROP_MOTOR_DRIVE_PIN1 6
#define DROP_MOTOR_DRIVE_PIN2 7
#define DROP_PWM_PIN1 8
#define DROP_PWM_PIN2 9

//ステアリング制御パラメータ
#define STEERING_STOP 128

//ステアリング用エンコーダピン
#define STEERING_PINA 34
#define STEERING_PINB 35

//ステアリング制御中信号出力ピン
#define IN_STEERING_CONTROL 13
/*------------------------------------------------------*/

// 制御用のゲイン設定
#define Kp 2     // pゲイン
#define Kd 5     // dゲイン
#define Kp_r 95  // 回転用pゲイン ex.350
#define Ki 40    // iゲイン ex.60

// 制御周期 Tc/1000 = 0.015
#define periodic_Time 0.015

// デバッグ用
#define debugLed_RED 40
#define debugLed_BLU 42
#define debugLed_GRE 44
#define debugLed_YEL 46

// 回転動作用 rad/s
#define target_yaw_rate 0.2  //目標角速度1ステップ分

// デッドゾーンのためのオフセット
#define offset 15

//ステアリング制御ゲイン
#define Kp_steering 3.0
#define Kd_steering 5.0

//ステアリング用エンコーダカウンタ
int enc_count = 0;

// ロボットの寸法(単位はメートル m)
#define LENGTH_FROM_CASTER 0.335
#define LENGTH_FROM_BASE 0.22

// 辞書風にデータを定義
typedef struct{
  double v_left_ratio_dict;
  double v_right_ratio_dict;
  double caster_angle_dict;
} data;

// 左から　左比率　右比率　キャスタ角度
const data dataDictionary[]{ 
  {1.0, 1.0, 0},            // 00 0000
  {2.0, 0.0, 56.70644},     // 01 0001
  {2.0, 0.0, 56.70644},     // 02 0010
  {2.0, 0.0, 56.70644},     // 03 0011
  {2.0, 0.0, 56.70644},     // 04 0100
  {1.0, 1.0, 0},            // 05 0101
  {1.33, 0.66, 26.91125},   // 06 0110
  {1.5, 0.5, 37.28433},     // 07 0111
  {0.0, 2.0, 0},            // 08 1000
  {0.66, 1.33, -26.91125},  // 09 1001
  {1.0, 1.0, 0},            // 10 1010
  {1.2, 0.8, 16.93788},     // 11 1011
  {0.0, 2.0, 0},            // 12 1100
  {0.5, 1.5, -37.28433},    // 13 1101
  {0.8, 1.2, -16.93788},    // 14 1110
  {1.0, 1.0, 0}             // 15 1111
};

// LCDを使うための設定
LiquidCrystal_I2C lcd(0x27, 20, 4);


/*-------------speed_control()の一部変数をグローバル変数に変更-------------*/
// 左右のモータスピード
int wheel_r_speed;
int wheel_l_speed;

//回転制御のためのステアリング制御
int in_steering_control = 0;

// ステアリング制御の時間計測
float start_time_steering_control = 0;
float last_time_steering_control = 0;
float in_steering_control_time = 0;

//ステアリングスピード
int steering_speed = STEERING_STOP;
/*-----------------------------------------------------------------------*/


void setup() {
  // I2C通信開始
  Wire.begin();
  delay(5);

  // Serial通信開始
  Serial.begin(115200);
  delay(5);

  // モータドライバのピン設定
  pinMode(MOTOR_DRIVE_PIN1, OUTPUT);
  pinMode(MOTOR_DRIVE_PIN2, OUTPUT);

  // ブラシ用モータのピン設定
  pinMode(DROP_MOTOR_DRIVE_PIN1, OUTPUT);
  pinMode(DROP_MOTOR_DRIVE_PIN2, OUTPUT);

  // モータ有効化
  digitalWrite(MOTOR_DRIVE_PIN1, LOW);
  digitalWrite(MOTOR_DRIVE_PIN2, LOW);
  digitalWrite(MOTOR_DRIVE_PIN1, HIGH);
  digitalWrite(MOTOR_DRIVE_PIN2, HIGH);

  digitalWrite(DROP_MOTOR_DRIVE_PIN1, LOW);
  digitalWrite(DROP_MOTOR_DRIVE_PIN2, LOW);
  digitalWrite(DROP_MOTOR_DRIVE_PIN1, HIGH);
  digitalWrite(DROP_MOTOR_DRIVE_PIN2, HIGH);

  pinMode(PWM_PIN1, OUTPUT);
  analogWrite(PWM_PIN1, 128);
  pinMode(PWM_PIN2, OUTPUT);
  analogWrite(PWM_PIN2, 128);

  pinMode(DROP_PWM_PIN1, OUTPUT);
  analogWrite(DROP_PWM_PIN1, 128);
  pinMode(DROP_PWM_PIN2, OUTPUT);
  analogWrite(DROP_PWM_PIN2, 128);

  // 制御信号読み取りピン設定
  pinMode(SERVO_ON, INPUT);
  pinMode(RIGHT_WHEEL_DIRECTION, INPUT);
  pinMode(RIGHT_WHEEL_SPEED_U, INPUT);
  pinMode(RIGHT_WHEEL_SPEED_D, INPUT);
  pinMode(LEFT_WHEEL_DIRECTION, INPUT);
  pinMode(LEFT_WHEEL_SPEED_U, INPUT);
  pinMode(LEFT_WHEEL_SPEED_D, INPUT);
  pinMode(POWDER_DROP, INPUT);

  //ステアリング用エンコーダピン設定
  pinMode(STEERING_PINA, INPUT);
  pinMode(STEERING_PINB, INPUT);
  attachInterrupt(digitalPinToInterrupt(STEERING_PINA), pulse_counter, CHANGE);

  //ステアリング制御中信号出力ピン設定
  pinMode(IN_STEERING_CONTROL, OUTPUT);
  digitalWrite(IN_STEERING_CONTROL, LOW);
  
  // デバッグLED設定
  pinMode(debugLed_RED, OUTPUT);
  pinMode(debugLed_BLU, OUTPUT);
  pinMode(debugLed_GRE, OUTPUT);
  pinMode(debugLed_YEL, OUTPUT);

  /*-----------------デバッグLEDチェック---------------------*/
  digitalWrite(debugLed_RED, HIGH);
  digitalWrite(debugLed_BLU, HIGH);
  digitalWrite(debugLed_GRE, HIGH);
  digitalWrite(debugLed_YEL, HIGH);

  delay(100);

  digitalWrite(debugLed_RED, LOW);
  digitalWrite(debugLed_BLU, LOW);
  digitalWrite(debugLed_GRE, LOW);
  digitalWrite(debugLed_YEL, LOW);

  delay(100);

  /*---------------------LCDチェック------------------------*/
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(5, 0);
  lcd.print("Prototype3");
  lcd.setCursor(0, 2);
  lcd.print("MODE: ");
  /*--------------------------------------------------------*/

  /*--------------------IMUの設定-----------------------------------------------*/
  // IMUとの通信確認
  // if (myIMU.begin() == false) {
  if (myIMU.begin(BNO08X_ADDR, Wire, BNO08X_INT, BNO08X_RST) == false) {

    Serial.println(
      "BNO08x not detected at default I2C address. Check your jumpers "
      "and the hookup guide. Freezing...");
    digitalWrite(debugLed_RED, HIGH);  // LED赤点灯
    lcd.setCursor(1, 0);
    lcd.print("An Error Occurred to:");
    lcd.setCursor(2, 0);
    lcd.print("IMU");
    lcd.setCursor(3, 0);
    lcd.print("Error Code: 1");
    while (1)
      ;
  }
  Serial.println("BNO08x found!");

  // Wire.setClock(400000); //Increase I2C data rate to 400kHz

  setReports();

  Serial.println("Reading events");

  /*----------------------------------------------------------------------------*/

  Serial.println("Setup Done. Waiting for signal...");
  Serial.flush();

  delay(100);

  // 割り込みの優先度設定
  NVIC_SetPriority((IRQn_Type)SysTick_IRQn, 0);
  NVIC_SetPriority((IRQn_Type)TC3_IRQn, 1);

  // 割り込みタイマーの設定
  startTimer(TC1, 0, TC3_IRQn, TC);

  
  serial_setup();
  
}


void pulse_counter() {
  if (digitalRead(STEERING_PINA) ^ digitalRead(STEERING_PINB)) {
    enc_count++;
  } else {
    enc_count--;
  }
}

// IMU設定関数
void setReports(void) {
  Serial.println("Setting desired reports");
  if (myIMU.enableGyroIntegratedRotationVector() == true) {
    Serial.println(F("Gryo Integrated Rotation vector enabled"));
    Serial.println(F("Output in form i, j, k, real, gyroX, gyroY, gyroZ"));
    digitalWrite(debugLed_YEL, LOW);
  } else {
    Serial.println("Could not enable gyro integrated rotation vector");
    digitalWrite(debugLed_YEL, HIGH);
  }
}

// タイマー用関数
void startTimer(Tc* tc, uint32_t channel, IRQn_Type irq, uint32_t mSec) {
  pmc_enable_periph_clk((uint32_t)irq);
  TC_Configure(tc, channel, TC_CMR_WAVE | TC_CMR_WAVSEL_UP_RC | TC_CMR_TCCLKS_TIMER_CLOCK1);
  uint32_t rc = (VARIANT_MCK / 2 / 1000) * mSec;
  TC_SetRC(tc, channel, rc);
  TC_Start(tc, channel);
  tc->TC_CHANNEL[channel].TC_IER = TC_IER_CPCS;
  tc->TC_CHANNEL[channel].TC_IDR = ~TC_IER_CPCS;
  NVIC_EnableIRQ(irq);
}

// タイマ割り込みで呼び出される関数
void TC3_Handler() {
  TC_GetStatus(TC1, 0);
  periodic_control();
}


/*-------------------------ここまで設定-----------------------------------------*/

void loop() {
}

// 周期制御
void periodic_control() {
  delay(10);

  float yaw_angle, yaw_rate;

  // 角速度・角度を取得
  if (myIMU.getSensorEvent() == true) {
    // is it the correct sensor data we want?
    if (myIMU.getSensorEventID() == SENSOR_REPORTID_GYRO_INTEGRATED_ROTATION_VECTOR) {
      // IMUから現在角度を取得
      yaw_angle = myIMU.getGyroIntegratedRVK() * 180.0 + 180.0;  // 0~360に変換

      // IMUから角速度取得
      yaw_rate = myIMU.getGyroIntegratedRVangVelZ();
    }
  }

  // サーボがオンなら
  if (digitalRead(SERVO_ON) == HIGH) {
    // 粉の排出 ← 変更？
    powder_drop();
　　
    //シリアル通信で情報を受け取りたいところに入れる
　　//関数がちゃんと処理できた場合は変数serial_data1, serial_data2, serial_data3に情報が入っている。
    //データ内容はGPIO.pdfを参考
    serial_com();
    
    if(digitalRead(EXECUTE_START)==HIGH){　//ラズパイから入力される動作開始信号
        
      check_serial_data(); //serial_data1, serial_data2, serial_data3のデータ確認用
      
      // 走行モードの取得 ← 変更？
      int mode = direction_control();
      
      // 走行モードに応じて制御 ← 変更？
      speed_control(mode, yaw_rate, yaw_angle);
      
      //動作時間を5秒と想定して模擬
      delay(5000);
      
      //命令を終えたことをラズパイに知らせる関数
      finish_instruction();
    }
  } else {
    // サーボ停止の場合
    analogWrite(DROP_PWM_PIN1, WHEEL_STOP);
    speed_control(4, yaw_rate, yaw_angle);
    // Serial.print("not kona ,");c:\Users\wakaba\Documents\Arduino\libraries\serial_spi\serial_spi.h
  }
}

// 粉の制御
void powder_drop() {
  if (digitalRead(POWDER_DROP) == HIGH) {
    analogWrite(DROP_PWM_PIN1, WHEEL_STOP + 100);
    /*
        Serial.print("kona");
        Serial.print(" ,");
        */
  } else {
    analogWrite(DROP_PWM_PIN1, WHEEL_STOP);
    /*
        Serial.print("not kona");
        Serial.print(" ,");
        */
  }
}

// LCDに文字を表示
void setDirectionLCD(String direction) {
  lcd.setCursor(6, 2);
  lcd.print(direction);
}

// 進行方向の制御
int direction_control() {
  // 前回進行方向モード
  static uint last_mode;

  // ビットの取得
  uint mode = digitalRead(RIGHT_WHEEL_DIRECTION) << 1 | digitalRead(LEFT_WHEEL_DIRECTION);

  // 進行方向モードが変わったら //使用中止
  /*if(mode != last_mode) {
        last_mode = mode;  // 前回の走行モードを保存

        Serial.print("mode change. reset yaw angle. mode = ");
        Serial.println(mode);

        //myIMU.softReset();
        //delay(10);
    }*/

  last_mode = mode;
  return mode;
}

// ステアリング制御
void steering_control(float target_enc_count, float enc_count) {
  digitalWrite(IN_STEERING_CONTROL, HIGH);

  wheel_r_speed = WHEEL_STOP;
  wheel_l_speed = WHEEL_STOP;
  steering_speed = STEERING_STOP + 0.5 * (target_enc_count - enc_count);
  last_time_steering_control = millis();
  in_steering_control_time = last_time_steering_control - start_time_steering_control;

  if (abs(target_enc_count - enc_count) < 30 && in_steering_control_time > 3000) {
    in_steering_control = 0;
    digitalWrite(IN_STEERING_CONTROL, LOW);
  }
}


// スピードの制御
void speed_control(unsigned int _mode, float _yaw_rate, float _yaw_angle) {
  static float target_angle = 180.0;  // 指示角度
  float angle;

  // 左右のモータスピード
  wheel_r_speed = 0;
  wheel_l_speed = 0;

  //ステアリングスピード
  steering_speed = STEERING_STOP;

  //回転制御のためのステアリング制御
  // in_steering_control = 0;

  //回転制御のための1つ前のモード記録
  static int pre_mode = 0;

  // 速度ステップを取得
  int step_r = digitalRead(RIGHT_WHEEL_SPEED_U) << 1 | digitalRead(RIGHT_WHEEL_SPEED_D);  // 停止00、低速01、中速10、高速11
  int step_l = digitalRead(LEFT_WHEEL_SPEED_U) << 1 | digitalRead(LEFT_WHEEL_SPEED_D);

  // I制御のための設定
  static float e_i = 0.0;

  // ステアリング制御の時間計測
  // start_time_steering_control = 0;
  // last_time_steering_control = 0;
  // in_steering_control_time = 0;

  angle = calibrate_angle(_yaw_angle, target_angle);
  // Serial.println(_yaw_rate, angle);

  if (_mode != pre_mode) {
    in_steering_control = 1;
    start_time_steering_control =  millis();
  }
  
  // 進行方向に応じて制御
  switch (_mode) {
    case 0:  // 前進
      
      /*************PD制御部分************
        -------------------------------
        | Ur = B-s-(θref - θ)Kp + ω*Kd |
        | Ul = B-s+(θref - θ)Kp - ω*Kd |
        -------------------------------
        U : 左右のモータに与える値(出力)
        B : モータが回転しない(中立)値
        s : 速度ステップ(3段階)
        θ : 現在の角度(入力)
        θref : 目標の角度(目標値)
        ω : 角速度
        Kp : Pゲイン
        Kd : Dゲイン
        ********************************/
      
      /*-------------------------------------------------------------------------*/
      // step_rとstep_lが同じか判定。同じなら前進、違うなら角度計算してカーブへ
      if (step_r==step_l) {
        if (in_steering_control == 1) {
          steering_control(0, enc_count);
        } else if (in_steering_control == 0) {
          //試作３号機用制御
          wheel_r_speed = WHEEL_STOP - step_r * WHEEL_SPEED_STEP_R + (target_angle - angle) * (Kp / step_r) - _yaw_rate * Kd;
          wheel_l_speed = WHEEL_STOP - step_l * WHEEL_SPEED_STEP_L - (target_angle - angle) * (Kp / step_l) + _yaw_rate * Kd;

          //ステアリング制御
          steering_speed = STEERING_STOP + Kp_steering * (target_angle - angle) + _yaw_rate * Kd_steering;
        } else {
        }

        digitalWrite(debugLed_GRE, HIGH);
        Serial.print("front");
        setDirectionLCD("front");

      } else {
        // ステップを4bitで取得
        unsigned int step = step_r << 2 | step_l;

        // 取得したステップに対応するキャスタ角度[deg]を取得し、エンコーダカウント値に変換
        double target_enc_count = dataDictionary[step].caster_angle_dict * 88.89;

        if (in_steering_control == 1) {
          steering_control(target_enc_count, enc_count);

          // digitalWrite(IN_STEERING_CONTROL, HIGH);
          // wheel_r_speed = WHEEL_STOP;
          // wheel_l_speed = WHEEL_STOP;
          // steering_speed = STEERING_STOP + 0.5 * (target_enc_count - enc_count);

          // // キャスタ回転のための時間を考慮
          // last_time_steering_control = millis();
          // in_steering_control_time = last_time_steering_control - start_time_steering_control;

          // if (abs(target_enc_count - enc_count) < 30 && in_steering_control_time > 3000) {
          //   in_steering_control = 0;
          //   digitalWrite(IN_STEERING_CONTROL, LOW);
          // }
        } else if (in_steering_control == 0) {
          //試作３号機用制御
          wheel_r_speed = WHEEL_STOP - step_r * WHEEL_SPEED_STEP_R;
          wheel_l_speed = WHEEL_STOP - step_l * WHEEL_SPEED_STEP_L;

          //ステアリング制御
          steering_speed = STEERING_STOP + 0.5 * (target_enc_count - enc_count);
        } else {
        }
        
        digitalWrite(debugLed_GRE, HIGH);
        Serial.print("curve");
        setDirectionLCD("curve");
      }
      /*-------------------------------------------------------------------------*/

      break;

    case 2:  //時計回り
      /*-------------------------------------------------------------------------*/
      if (in_steering_control == 1) {
        steering_control(8000, enc_count);

        // digitalWrite(IN_STEERING_CONTROL, HIGH);
        // wheel_r_speed = WHEEL_STOP;
        // wheel_l_speed = WHEEL_STOP;
        // steering_speed = STEERING_STOP + 0.5 * (8000 - enc_count);
        // last_time_steering_control = millis();
        // in_steering_control_time = last_time_steering_control - start_time_steering_control;

        // // Serial.println("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq");
        // if (abs(8000 - enc_count) < 30 && in_steering_control_time > 3000) {
        //   // Serial.println("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
        //   Serial.print(enc_count);
        //   Serial.print(",");
        //   Serial.print(in_steering_control_time);
        //   Serial.println("");

        //   in_steering_control = 0;
        //   digitalWrite(IN_STEERING_CONTROL, LOW);
        // }
      } else if (in_steering_control == 0) {
        //制御なし
        wheel_r_speed = WHEEL_STOP - WHEEL_SPEED_STEP_ROT;
        wheel_l_speed = WHEEL_STOP + WHEEL_SPEED_STEP_ROT;
        steering_speed = STEERING_STOP + 0.5 * (8000 - enc_count);

        target_angle = _yaw_angle;  // 指示角度の更新
      } else {
      }
      /*-------------------------------------------------------------------------*/

      digitalWrite(debugLed_GRE, HIGH);
      Serial.print("right");
      setDirectionLCD("right");

      break;

    case 1:  //反時計回り
      /*-------------------------------------------------------------------------*/
      if (in_steering_control == 1) {
        steering_control(8000, enc_count);

        // digitalWrite(IN_STEERING_CONTROL, HIGH);
        // wheel_r_speed = WHEEL_STOP;
        // wheel_l_speed = WHEEL_STOP;
        // steering_speed = STEERING_STOP + 0.5 * (8000 - enc_count);
        // last_time_steering_control = millis();
        // in_steering_control_time = last_time_steering_control - start_time_steering_control;

        // // Serial.println("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq");
        // if (abs(8000 - enc_count) < 30 && in_steering_control_time > 3000 ) {
        //   // Serial.println("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
        //   Serial.print(enc_count);
        //   Serial.print(",");
        //   Serial.print(in_steering_control_time);
        //   Serial.println("");

        //   in_steering_control = 0;
        //   digitalWrite(IN_STEERING_CONTROL, LOW);
        // }
      } else if (in_steering_control == 0) {

        //制御なし
        wheel_r_speed = WHEEL_STOP + WHEEL_SPEED_STEP_ROT;
        wheel_l_speed = WHEEL_STOP - WHEEL_SPEED_STEP_ROT;
        steering_speed = STEERING_STOP + 0.5 * (8000 - enc_count);

        target_angle = _yaw_angle;  // 指示角度の更新
      } else {
      }
      /*-------------------------------------------------------------------------*/

      digitalWrite(debugLed_GRE, HIGH);
      Serial.print("left");
      setDirectionLCD(" left");

      break;

    case 3:  // 後進
      /*----------------------------------------------------------------------------------------------------------------*/
      if (in_steering_control == 1) {
        steering_control(0, enc_count);

        // digitalWrite(IN_STEERING_CONTROL, HIGH);
        // wheel_r_speed = WHEEL_STOP;
        // wheel_l_speed = WHEEL_STOP;
        // steering_speed = STEERING_STOP + 0.5 * (0 - enc_count);
        // // Serial.println("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq");
        // last_time_steering_control = millis();
        // in_steering_control_time = last_time_steering_control - start_time_steering_control;

        // if (abs(0 - enc_count) < 30  && in_steering_control_time > 3000 ) {
        //   // Serial.println("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
        //   in_steering_control = 0;
        //   digitalWrite(IN_STEERING_CONTROL, LOW);
        // }
      } else if (in_steering_control == 0) {
        //試作３号機用制御
        wheel_r_speed = WHEEL_STOP + step_r * WHEEL_SPEED_STEP_R + (target_angle - angle) * (Kp / step_r) + _yaw_rate * Kd;

        wheel_l_speed = WHEEL_STOP + step_l * WHEEL_SPEED_STEP_L - (target_angle - angle) * (Kp / step_r) - _yaw_rate * Kd;

        //ステアリング制御
        steering_speed = STEERING_STOP - Kp_steering * (target_angle - angle) - _yaw_rate * Kd_steering;

        e_i = 0.0;

      } else {
      }
      /*----------------------------------------------------------------------------------------------------------------*/

      digitalWrite(debugLed_GRE, HIGH);
      //Serial.print("back");
      //setDirectionLCD(" back");

      break;

    case 4:  // 停止
      if (in_steering_control == 1) {
        steering_control(0, enc_count);

        // digitalWrite(IN_STEERING_CONTROL, HIGH);
        // wheel_r_speed = WHEEL_STOP;
        // wheel_l_speed = WHEEL_STOP;
        // steering_speed = STEERING_STOP + 0.5 * (0 - enc_count);
        // last_time_steering_control = millis();
        // in_steering_control_time = last_time_steering_control - start_time_steering_control;

        // // Serial.println("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq");
        // if (abs(0 - enc_count) < 30 && in_steering_control_time > 3000) {
        //   // Serial.println("aaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaa");
        //   in_steering_control = 0;
        //   digitalWrite(IN_STEERING_CONTROL, LOW);
        // }
      } else if (in_steering_control == 0) {
        // e_i = 0.0;

        wheel_r_speed = 128;
        wheel_l_speed = 128;
        steering_speed = STEERING_STOP;
        
        target_angle = _yaw_angle;  // 指示角度の更新
      } else {
      }

      digitalWrite(debugLed_GRE, LOW);
      //Serial.print("stop ");
      setDirectionLCD(" stop");

      break;

    default:  // 異常
      Serial.print("Error! Motor direction signal is wrong");
      Serial.print("mode = ");
      Serial.println(_mode);
      digitalWrite(debugLed_GRE, LOW);
      digitalWrite(debugLed_YEL, HIGH);
      setDirectionLCD("Error!!");
      wheel_move(128, 128);

      break;
  }

  pre_mode = _mode;
/*
  Serial.print(",");
  Serial.print(millis());
  Serial.print(",");
  Serial.print(step_r);
  Serial.print(",");
  Serial.print(step_l);
  Serial.print("| ");
  Serial.print(_yaw_rate);
  Serial.print(",");
  Serial.print(angle);
  Serial.print(",");
  Serial.print(target_angle);
  Serial.print(",");
  Serial.print(wheel_r_speed);
  Serial.print(",");
  Serial.print(wheel_l_speed);
  Serial.print(",");
  Serial.print(steering_speed);
  Serial.print(",");
  Serial.print(enc_count);
  Serial.print(",");
  Serial.print(in_steering_control);
  Serial.print(",");
  Serial.print(in_steering_control_time);
  Serial.println();
*/
  // ホイールにつながっているモータを動かす
  wheel_move(wheel_r_speed, wheel_l_speed);
  steering_move(steering_speed);
}

void steering_move(int input) {
  /*-----リミッタ-----*/
  if (input >= 254)
    input = 254;
  else if (input <= 0)
    input = 0;
  else {}
  /*------------------*/

  analogWrite(DROP_PWM_PIN2, input);
}

// ホイール回転
void wheel_move(int input_r, int input_l) {
  /*-----リミッタ-----*/
  if (input_r >= 254)
    input_r = 254;
  else if (input_r <= 0)
    input_r = 0;
  if (input_l >= 254)
    input_l = 254;
  else if (input_l <= 0)
    input_l = 0;
  /*------------------*/

  // モータ駆動
  analogWrite(PWM_PIN1, input_r);
  analogWrite(PWM_PIN2, input_l);
}

// デバッグLED
void debugLed(bool r, bool b, bool g, bool y) {
  digitalWrite(debugLed_RED, r);
  digitalWrite(debugLed_BLU, b);
  digitalWrite(debugLed_GRE, g);
  digitalWrite(debugLed_YEL, y);
}

// 0,360度またぎ問題
float calibrate_angle(float now_angle, float target_angle) {
  float return_angle;
  if (abs(target_angle - now_angle) > 180) {  // 0度をまたいだら
    if (now_angle > 180) {                    // -方向にまたいだら
      return_angle = now_angle - 360;         // 0~-180度として処理

    } else if (now_angle < 180) {      //+方向にまたいだら
      return_angle = 360 + now_angle;  // 360~540度として処理

    } else {
      return_angle = now_angle;
    }
  } else {
    return now_angle;
  }
  return return_angle;
}

