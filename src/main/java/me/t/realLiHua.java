package me.t;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.telegram.telegrambots.longpolling.TelegramBotsLongPollingApplication;

public class realLiHua {
    static final Logger logger = LoggerFactory.getLogger(realLiHua.class);
  public static void main(String[] args) {
    String botToken = args[0];
    try (TelegramBotsLongPollingApplication botsApplication =
        new TelegramBotsLongPollingApplication()) {
      botsApplication.registerBot(botToken, new MyBot(botToken));
	    logger.debug("Did it again!");
      Thread.currentThread().join();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
