//ヘッダーファイルが複数回インクルードされるのを防ぐためのプリプロセッサディレクティブ（事前処理指示）です
#ifndef serial_spi_h
#define  serial_spi_h

// Arduinoの基本的な機能を利用するためのヘッダファイルをインクルードします。
#include <Arduino.h>
#include <SPI.h>
#define SERIAL_ON 30
#define EXECUTE_END 32
#define EXECUTE_START 24  
#define SS_PIN 10


uint16_t serial_data1, serial_data2, serial_data3;
int receive_flag;

// 自分の作成したい関数を定義します。関数の処理は別ファイルで書きます。
void serial_setup(){
  receive_flag=0;
  pinMode(SERIAL_ON, INPUT);
  pinMode(EXECUTE_START, INPUT);
  pinMode(EXECUTE_END, OUTPUT);
  Serial.begin(115200);
  while (!Serial);

  pinMode(SS_PIN, INPUT);  // スレーブなので SS を入力に
  SPI.begin(SS_PIN);       // スレーブ用に開始（Due専用）

  // SPI0をスレーブとして構成
  REG_SPI0_CR = SPI_CR_SWRST;               // ソフトウェアリセット
  REG_SPI0_CR = SPI_CR_SPIEN;               // SPI有効化
  REG_SPI0_MR = SPI_MR_MODFDIS;             // モードフォルト無効、スレーブ動作
  REG_SPI0_CSR = 0;                          // MODE0（CPOL=0, CPHA=0）、8bit
  serial_data1=0;
  serial_data2=0;
  serial_data3=0;
  Serial.println("SPI Slave ready");

}


void serial_com(){

	while(digitalRead(SERIAL_ON) == HIGH){
		
	 if (digitalRead(SS_PIN) == LOW) {

			 // 5バイトのデータ受信
    		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0 &&digitalRead(SERIAL_ON) == HIGH);
    		uint8_t byte1 = REG_SPI0_RDR & 0xFF;
    		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		uint8_t byte2 = REG_SPI0_RDR & 0xFF;
		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0 &&digitalRead(SERIAL_ON) == HIGH);
    		uint8_t byte3 = REG_SPI0_RDR & 0xFF;
    		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		uint8_t byte4 = REG_SPI0_RDR & 0xFF;   
		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		uint8_t byte5 = REG_SPI0_RDR & 0xFF;   		

    		serial_data1 = byte1;
		serial_data2 = (byte3 << 8) | byte2;
		serial_data3 = (byte5 << 8) | byte4;

    		// 受信データを送り返す
    		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte1;
    		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte2;
		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte3;
    		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte4;
		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte5;

		// 5バイトのダミーデータ受信
    		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		byte1 = REG_SPI0_RDR & 0xFF;
    		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		byte2 = REG_SPI0_RDR & 0xFF;
		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		byte3 = REG_SPI0_RDR & 0xFF;
    		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		byte4 = REG_SPI0_RDR & 0xFF;
		while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    		byte5 = REG_SPI0_RDR & 0xFF;

    		// 5バイトのダミーデータを送り返し
    		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte1;   
    		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte2;
       		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte3;   
    		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte4;
		while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    		REG_SPI0_TDR = byte5;
    	}

    }
}


void check_serial_data(){
	Serial.print("Receive data1:");
	Serial.println(serial_data1);
	Serial.print("Receive data2:");
	Serial.println(serial_data2);
	Serial.print("Receive data3:");
	Serial.println(serial_data3);
}


void finish_instruction(){

	while(digitalRead(EXECUTE_START) == HIGH){
		digitalWrite(EXECUTE_END, HIGH);
	}
	digitalWrite(EXECUTE_END, LOW);
	Serial.println("Finish instruction");

}
// ヘッダファイルの終わりを示すプリプロセッサディレクティブです。
#endif