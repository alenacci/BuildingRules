package com.hpps.danger.user;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.os.Vibrator;

public class NotificationsHandler {

	boolean notificationDisplayed = false;

	int lastTimestamp = 0;
	
	public void reset(){
		 notificationDisplayed = false;
		 lastTimestamp = 0;
	}
	
	public void readFromJson(Context c,JSONArray array){

		for (int i = 0; i < array.length(); i++) {
			JSONObject o;
			try {
				o = array.getJSONObject(i);
				String notificationType = o.getString("type");
				
				
				//Update the timestamp if greater
				int timestamp = Integer.parseInt(o.getString("timestamp"));
				if(timestamp > lastTimestamp){
					lastTimestamp = timestamp;
				}
				
				if(notificationType.equals("danger")) {
					handleDanger(c);
				} else if (notificationType.equals("action-record_audio")){
					handleRecordAudio();
				}
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}
		
	}
	
	public int getTimestamp() {
		return lastTimestamp;
	}
	
	private void handleDanger(Context c) {
		if(!notificationDisplayed) {
			//Trigger notification
			Intent dialogIntent = new Intent(c, UserDangerActivity.class);
			dialogIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
			c.startActivity(dialogIntent);

			//Make the device vibrate
			Vibrator v = (Vibrator) c.getSystemService(Context.VIBRATOR_SERVICE);
			// Vibrate for 500 milliseconds
			v.vibrate(500);

			notificationDisplayed = true;
		}
	}
	
	private void handleRecordAudio(){
		AudioSensing a = new AudioSensing();
		a.start();
	}
}

