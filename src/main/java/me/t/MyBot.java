package me.t;

//import java.text.DateFormat;
//import java.text.SimpleDateFormat;
//import java.util.Date;
import org.telegram.telegrambots.client.okhttp.OkHttpTelegramClient;
import org.telegram.telegrambots.longpolling.util.LongPollingSingleThreadUpdateConsumer;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

public class MyBot extends Base implements LongPollingSingleThreadUpdateConsumer {
  public MyBot(String botToken) {
    super(botToken);
  }

  public void consume(Update update) {
    super.consume(update);
    this.answer = this.message_text;
    SendMessage message =
          SendMessage.builder().chatId(this.chat_id).text(this.answer).build();
      log();
      try {
        telegramClient.execute(message);
      } catch (TelegramApiException e) {
        e.printStackTrace();
      }
  }
}
