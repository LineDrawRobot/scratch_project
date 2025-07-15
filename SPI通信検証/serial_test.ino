// SPI スレーブ用コード（Arduino Due）
/*
int i,flag;
void setup() {
  Serial.begin(115200);
  while (!Serial);

  // SPI用ピンの初期化
  pinMode(MISO, OUTPUT); // MISO: Master In Slave Out
  pinMode(MOSI, INPUT);
  pinMode(SCK, INPUT);
  pinMode(SS, INPUT);    // スレーブでは SS を必ず INPUT に！

  // SPIをリセットしてから有効化
  REG_SPI0_CR = SPI_CR_SWRST;     // ソフトリセット
  REG_SPI0_CR = SPI_CR_SPIEN;     // SPI有効化

  // モード設定：スレーブ・MODFエラー無効
  REG_SPI0_MR = SPI_MR_MODFDIS;   // スレーブ＋モードフォールト無効

  // SPI通信モード設定（MODE0）
  REG_SPI0_CSR = SPI_CSR_NCPHA | SPI_CSR_BITS_8_BIT; // 立ち上がりサンプリング・8ビット転送

  Serial.println("SPI slave ready (Due)");
  i=0;
  flag=0;
}

void loop() {
  // RDRFビットが立ってるか確認（受信完了）
  if (digitalRead(SS) == LOW) {
    if(flag==0){ i=i+1; flag=1;}
    Serial.print(i);
    Serial.print(":");
    Serial.println(REG_SPI0_SR);
  }else{
    if(flag==1){
     Serial.print(":");
    Serial.println(REG_SPI0_SR); 
    while (!(REG_SPI0_SR & SPI_SR_TDRE));
    REG_SPI0_TDR = 0xFF;
    flag=0;
    }
  }
  if (REG_SPI0_SR & SPI_SR_RDRF) {
    uint16_t inData = REG_SPI0_RDR & 0xFF; // 8bit受信
    Serial.print("Received: ");
    Serial.println(inData, HEX);

    uint16_t outData = inData + 1; // 応答値：受信+1（例）

    // 送信レジスタが空か確認してから書き込む
    while (!(REG_SPI0_SR & SPI_SR_TDRE));
    REG_SPI0_TDR = outData;

    Serial.print("Replied: ");
    Serial.println(outData, HEX);
  }

}
*/
#define SS_PIN 10  // CE0 に対応。必ず OUTPUT ではなく INPUT に！
#define SERIAL_ON 30
#include <SPI.h>

void setup() {
  Serial.begin(115200);
  while (!Serial);
  pinMode(SERIAL_ON, INPUT);
  pinMode(SS_PIN, INPUT);  // スレーブなので SS を入力に
  SPI.begin(SS_PIN);       // スレーブ用に開始（Due専用）

  // SPI0をスレーブとして構成
  REG_SPI0_CR = SPI_CR_SWRST;               // ソフトウェアリセット
  REG_SPI0_CR = SPI_CR_SPIEN;               // SPI有効化
  REG_SPI0_MR = SPI_MR_MODFDIS;             // モードフォルト無効、スレーブ動作
  REG_SPI0_CSR = 0;                          // MODE0（CPOL=0, CPHA=0）、8bit
 

  
   Serial.println("SPI Slave ready");
}

uint16_t send_data;
int timer=0;

void loop() {

  timer++;
  
  if (digitalRead(SS_PIN) == LOW) {
    
    // 2バイトのデータ受信
    while ((REG_SPI0_SR & SPI_SR_RDRF) == 0 &&digitalRead(SERIAL_ON) == HIGH);
    uint8_t byte1 = REG_SPI0_RDR & 0xFF;
    while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    uint8_t byte2 = REG_SPI0_RDR & 0xFF;
     
    send_data = (byte2 << 8) | byte1;
    // 受信データを送り返す
    while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    REG_SPI0_TDR = byte1;
    while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    REG_SPI0_TDR = byte2;

    // 2バイトのダミーデータ受信
    while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    byte1 = REG_SPI0_RDR & 0xFF;
    while ((REG_SPI0_SR & SPI_SR_RDRF) == 0&&digitalRead(SERIAL_ON) == HIGH);
    byte2 = REG_SPI0_RDR & 0xFF;
    // 2バイトのダミーデータを送り返し
    while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    REG_SPI0_TDR = byte1;   
    while (!(REG_SPI0_SR & SPI_SR_TDRE)&&digitalRead(SERIAL_ON) == HIGH);
    REG_SPI0_TDR = byte2;         
  }
  if(timer%1000000==0)Serial.println(send_data, DEC); 
}