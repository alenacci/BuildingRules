package com.hpps.danger;

import com.hpps.danger.buildingmanager.BulletinReader;
import com.hpps.danger.user.NotificationsHandler;

import android.app.Application;

public class DangerApplication extends Application {

	private static DangerApplication app = null;

	private String ip;
	private BulletinReader bulletinReader;
	private NotificationsHandler notificationsHandler;
	public String DANGER_SERVER_API,RULES_SERVER_API;

	@Override
	public void onCreate()
	{
		super.onCreate();

		app = this;
		bulletinReader = new BulletinReader();
		notificationsHandler = new NotificationsHandler();
	}

	public static DangerApplication getApp() {
		return app;
	}

	public void setIp(String ip){
		this.ip = ip;
		this.DANGER_SERVER_API = "http://" + this.ip + ":2001/api/";
		this.RULES_SERVER_API = "http://" + this.ip + ":5003/api/";
	}
	
	public BulletinReader getBulletinReader() {
			return bulletinReader;
	}
	
	public NotificationsHandler getNotificationsHandler() {
		return notificationsHandler;
	}

}
