package me.t;

import org.telegram.telegrambots.longpolling.TelegramBotsLongPollingApplication;

public class realLiHua {
  public static void main(String[] args) {
    String botToken = args[0];
    try (TelegramBotsLongPollingApplication botsApplication =
        new TelegramBotsLongPollingApplication()) {
      botsApplication.registerBot(botToken, new MyBot(botToken));
	System.out.println("Bot successfully started!");
      Thread.currentThread().join();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
