package com.hpps.danger.user;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.IBinder;
import android.os.Looper;
import android.os.Message;
import android.os.PowerManager;
import android.os.Process;
import android.os.SystemClock;
import android.os.Vibrator;
import android.util.Log;
import android.widget.Toast;

import com.hpps.danger.DangerApplication;

public class UserNotificationService extends Service {
	private Looper mServiceLooper;
	private ServiceHandler mServiceHandler;

	public String DANGER_SERVER_API;

	public static final int POLLING_TIME = 5000;
	
	private PowerManager.WakeLock wl;
	
	public static boolean isStarted = false;

	
	// Handler that receives messages from the thread
	private final class ServiceHandler extends Handler {
		public ServiceHandler(Looper looper) {
			super(looper);
		}

		@Override
		public void handleMessage(Message msg) {

			long endTime = System.currentTimeMillis() + 1200*1000;
			while (/*System.currentTimeMillis() < endTime && */isStarted) {
				synchronized (this) {
					try {
						String jsonString = readDangerStatus();
						JSONObject jsonObject = new JSONObject(jsonString);

						
						//If there are new notifications, pass them to the notification handler
						if(jsonObject.getString("new_notifications").equals("True") ){
							JSONArray array = jsonObject.getJSONArray("notifications");
							DangerApplication.getApp().getNotificationsHandler().readFromJson(UserNotificationService.this, array);
						}
					} catch (Exception e) {
						e.printStackTrace();
					}
				}


				SystemClock.sleep(POLLING_TIME);
			}
		}

		/**
		 * Request the list of the last notifications
		 * @return
		 */
		private String readDangerStatus() {
			StringBuilder builder = new StringBuilder();
			HttpClient client = new DefaultHttpClient();
			HttpPost httpPost = new HttpPost(DANGER_SERVER_API + "user/get_notifications");

			HashMap<String,String> postMessage = new HashMap<String,String>();
			
			NotificationsHandler notif = DangerApplication.getApp().getNotificationsHandler();
			
			
			postMessage.put("timestamp", Integer.toString(notif.getTimestamp()));

			try {

				JSONObject holder = new JSONObject(postMessage);
				//passes the results to a string builder/entity
				StringEntity se = new StringEntity(holder.toString());
				httpPost.setEntity(se);
				httpPost.setHeader("Accept", "application/json");
				httpPost.setHeader("Content-type", "application/json");
				HttpResponse response = client.execute(httpPost);
				StatusLine statusLine = response.getStatusLine();
				int statusCode = statusLine.getStatusCode();
				if (statusCode == 200) {
					HttpEntity entity = response.getEntity();
					InputStream content = entity.getContent();
					BufferedReader reader = new BufferedReader(new InputStreamReader(content));
					String line;
					while ((line = reader.readLine()) != null) {
						builder.append(line);
					}
				} else {
					Log.e("REQUEST", "Failed to contact server");
				}
			} catch (ClientProtocolException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
			return builder.toString();
		}
	}

	@Override
	public void onCreate() {

		
		HandlerThread thread = new HandlerThread("ServiceStartArguments",
				Process.THREAD_PRIORITY_BACKGROUND);
		thread.start();

		
		
		mServiceLooper = thread.getLooper();
		mServiceHandler = new ServiceHandler(mServiceLooper);
	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
		
		
		Toast.makeText(this, "service starting", Toast.LENGTH_SHORT).show();
		isStarted = true;

		DangerApplication.getApp().getNotificationsHandler().reset();
		
		DANGER_SERVER_API = DangerApplication.getApp().DANGER_SERVER_API;
		
		Message msg = mServiceHandler.obtainMessage();
		msg.arg1 = startId;
		mServiceHandler.sendMessage(msg);

		PowerManager pm = (PowerManager)getSystemService(Context.POWER_SERVICE);
		wl = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "user_notification_wakelock");
		wl.acquire();
		
		// If we get killed, after returning from here, restart
		return START_STICKY;
	}

	@Override
	public IBinder onBind(Intent intent) {
		// We don't provide binding, so return null
		return null;
	}

	@Override
	public void onDestroy() {
		Toast.makeText(this, "service done", Toast.LENGTH_SHORT).show();
		isStarted = false;
		wl.release();
	}


	private static JSONObject getJsonObjectFromMap(Map params) throws JSONException {

		//all the passed parameters from the post request
		//iterator used to loop through all the parameters
		//passed in the post request
		Iterator iter = params.entrySet().iterator();

		//Stores JSON
		JSONObject holder = new JSONObject();

		//using the earlier example your first entry would get email
		//and the inner while would get the value which would be 'foo@bar.com' 
		//{ fan: { email : 'foo@bar.com' } }

		//While there is another entry
		while (iter.hasNext()) 
		{
			//gets an entry in the params
			Map.Entry pairs = (Map.Entry)iter.next();

			//creates a key for Map
			String key = (String)pairs.getKey();

			//Create a new map
			Map m = (Map)pairs.getValue();   

			//object for storing Json
			JSONObject data = new JSONObject();

			//gets the value
			Iterator iter2 = m.entrySet().iterator();
			while (iter2.hasNext()) 
			{
				Map.Entry pairs2 = (Map.Entry)iter2.next();
				data.put((String)pairs2.getKey(), (String)pairs2.getValue());
			}

			//puts email and 'foo@bar.com'  together in map
			holder.put(key, data);
		}
		return holder;
	}
}