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

public class Base implements LongPollingSingleThreadUpdateConsumer {
  protected final TelegramClient telegramClient;
  protected String first_name;
  protected String last_name;
  protected String username;
  protected long user_id;
  protected long chat_id;
  protected String message_text;
  protected String answer;

  public Base(String botToken) {
    telegramClient = new OkHttpTelegramClient(botToken);
  }

  @Override
  public void consume(Update update) {
    if (update.hasMessage()) {
      this.first_name = update.getMessage().getChat().getFirstName();
      this.last_name = update.getMessage().getChat().getLastName();
      this.username = update.getMessage().getChat().getUserName();
      this.user_id = update.getMessage().getChat().getId();
      this.chat_id = update.getMessage().getChatId();
    if (update.getMessage().hasText()) {
      this.message_text = update.getMessage().getText();
	    }
    }
  }

  protected void log() {
    System.out.println("\n----------------------------");
    DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    Date date = new Date();
    System.out.println(dateFormat.format(date));
    System.out.println(
        String.format(
            "Message from %s %s. (id = %s)", this.first_name, this.last_name, this.user_id));
    System.out.println(String.format(" Text - %s", this.message_text));
    System.out.println("Bot answer: \n Text - " + this.answer);
  }
}
