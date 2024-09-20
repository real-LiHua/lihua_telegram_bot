package me.t;
import org.telegram.telegrambots.longpolling.TelegramBotsLongPollingApplication;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public class realLiHua {
    public static void main(String[] args) {
	String botToken = args[0];
	try (TelegramBotsLongPollingApplication botsApplication = new TelegramBotsLongPollingApplication()) {
	    botsApplication.registerBot(botToken, new MyBot(botToken));
	    Thread.currentThread().join();
	} catch (Exception e) {
	    e.printStackTrace();
	}
    }
}
