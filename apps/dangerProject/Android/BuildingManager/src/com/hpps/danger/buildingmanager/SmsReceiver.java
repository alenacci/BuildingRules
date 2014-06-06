package com.hpps.danger.buildingmanager;

import com.hpps.danger.DangerApplication;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.telephony.SmsMessage;
import android.util.Log;
import android.widget.Toast;

public class SmsReceiver extends BroadcastReceiver {

	public final String SMS_KEYWORD = "SMS_DANGER";
	
	// Get the object of SmsManager
	final SmsManager sms = SmsManager.getDefault();
	
	@Override
	public void onReceive(Context context, Intent intent) {
		// Retrieves a map of extended data from the intent.
		final Bundle bundle = intent.getExtras();
		 
		try {
		     
		    if (bundle != null) {
		         
		        final Object[] pdusObj = (Object[]) bundle.get("pdus");
		         
		        for (int i = 0; i < pdusObj.length; i++) {
		             
		            SmsMessage currentMessage = SmsMessage.createFromPdu((byte[]) pdusObj[i]);
		            String phoneNumber = currentMessage.getDisplayOriginatingAddress();
		             
		            String senderNum = phoneNumber;
		            String message = currentMessage.getDisplayMessageBody();
		 
		            Log.i("SmsReceiver", "senderNum: "+ senderNum + "; message: " + message);
		             
		 
		           // Show alert
//		            int duration = Toast.LENGTH_LONG;
//		            Toast toast = Toast.makeText(context, "senderNum: "+ senderNum + ", message: " + message, duration);
//		            toast.show();
		             
		            decodeSms(context, message);
		        } 
		      } 
		 
		} catch (Exception e) {
		    Log.e("SmsReceiver", "Exception smsReceiver" +e);
		     
		}

	}
	
	
	private void decodeSms(Context c, String text) {
		//we expect the first word to be a keyword
		String words[] = text.split(" ",2);
		if(words.length > 1){
			String firstWord = words[0];
			
			if(firstWord.equals(SMS_KEYWORD)) {
				String json = words[1];
				BulletinReader bReader = DangerApplication.getApp().getBulletinReader();
				bReader.decodeJson(c, json);
			}
			
		}
	}
	

}
