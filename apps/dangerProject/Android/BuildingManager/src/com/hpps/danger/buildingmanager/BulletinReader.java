package com.hpps.danger.buildingmanager;

import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.content.Intent;
import android.os.Vibrator;

/**
 * THis class receive all the bullettine
 * as form of json and read it.
 * It takes care of trigger the adequate
 * actions
 */
public class BulletinReader {

	private boolean alertDisplayed = false;

	public void reset() {
		 alertDisplayed = false;
	}
	
	/**
	 * This method decode the alert json and 
	 * launch the alert activity
	 * @param jsonString
	 */
	public void decodeJson(Context c, String jsonString ) {

		try {
			JSONObject jsonObject = new JSONObject(jsonString);
			if(jsonObject.getString("status").equals("ALERT") && !alertDisplayed){
				//trigger Notification
				Intent dialogIntent = new Intent(c, ManagerDangerActivity.class);
				dialogIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

				dialogIntent.putExtra("building", jsonObject.getString("building"));
				dialogIntent.putExtra("room", jsonObject.getString("room"));
				dialogIntent.putExtra("description", jsonObject.getString("description"));

				c.startActivity(dialogIntent);

				//Make the device vibrate
				Vibrator v = (Vibrator) c.getSystemService(Context.VIBRATOR_SERVICE);
				// Vibrate for 500 milliseconds
				v.vibrate(1500);

				alertDisplayed = true;
			}
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
