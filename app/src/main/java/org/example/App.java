package org.example;
import org.telegram.telegrambots.longpolling.TelegramBotsLongPollingApplication;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public class App {
    public static void main(String[] args) {
	String botToken = args[0];
	try (TelegramBotsLongPollingApplication botsApplication = new TelegramBotsLongPollingApplication()) {
	    botsApplication.registerBot(botToken, new MyBot(botToken));
	    System.out.println("MyBot successfully started!");
	    Thread.currentThread().join();
	} catch (Exception e) {
	    e.printStackTrace();
	}
    }
}
