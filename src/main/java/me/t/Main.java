package me.t;

import org.telegram.telegrambots.meta.api.methods.description.SetMyDescription;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

public class Main extends Base {
  public Main(TelegramClient telegramClient, String botUsername) {
    super(telegramClient, botUsername);
  }

  public void onRegister() {
    SetMyDescription description = SetMyDescription.builder().description("Test").build();
    this.silent.execute(description);
    super.onRegister();
  }

  public void consume(Update update) {
    super.consume(update);
    this.answer = this.message_text;
    SendMessage message = SendMessage.builder().chatId(this.chat_id).text(this.answer).build();
    log();
    try {
      telegramClient.execute(message);
    } catch (TelegramApiException e) {
      e.printStackTrace();
    }
  }
}
