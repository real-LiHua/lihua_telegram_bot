package me.t;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.telegram.telegrambots.client.okhttp.OkHttpTelegramClient;
import org.telegram.telegrambots.longpolling.util.LongPollingSingleThreadUpdateConsumer;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

public class MyBot implements LongPollingSingleThreadUpdateConsumer {
  private final TelegramClient telegramClient;
   private  String first_name;
     private  String last_name;
    private   String username;
   private    long user_id;
   private    String message_text;
  private     long chat_id;
    private   String answer;

  public MyBot(String botToken) {
    telegramClient = new OkHttpTelegramClient(botToken);
  }

  @Override
  public void consume(Update update) {
    if (update.hasMessage() && update.getMessage().hasText()) {
      this.first_name = update.getMessage().getChat().getFirstName();
      this.last_name = update.getMessage().getChat().getLastName();
      this.username = update.getMessage().getChat().getUserName();
      this.user_id = update.getMessage().getChat().getId();
      this.message_text = update.getMessage().getText();
      this.chat_id = update.getMessage().getChatId();
      this.answer = message_text;

      SendMessage message = SendMessage.builder().chatId(this.chat_id).text(this.message_text).build();
      log();
      try {
        telegramClient.execute(message);
      } catch (TelegramApiException e) {
        e.printStackTrace();
      }
    }
  }

  private void log() {
    System.out.println("\n ----------------------------");
    DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    Date date = new Date();
    System.out.println(dateFormat.format(date));
    System.out.println(
        String.format("Message from %s %s. (id = %s)", this.first_name, this.last_name, this.user_id));
    System.out.println(String.format(" Text - %s", this.message_text));
    System.out.println("Bot answer: \n Text - " + this.answer);
  }
}
