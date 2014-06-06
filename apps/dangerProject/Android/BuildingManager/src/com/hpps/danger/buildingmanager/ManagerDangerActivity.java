package com.hpps.danger.buildingmanager;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

import com.hpps.danger.DangerApplication;

/**
 */
public class ManagerDangerActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		setContentView(R.layout.manager_activity_danger);

		Button confirmButton = (Button)findViewById(R.id.confirm_button);
		TextView buildingText = (TextView)findViewById(R.id.building_text);
		TextView roomText = (TextView)findViewById(R.id.room_text);
		TextView descriptionText = (TextView)findViewById(R.id.danger_text);

		buildingText.setText("Building: " + getIntent().getExtras().getString("building"));
		roomText.setText("CSE: " + getIntent().getExtras().getString("room"));
		descriptionText.setText("Description: " + getIntent().getExtras().getString("description"));

		Button listenButton = (Button)findViewById(R.id.listen_button);

		confirmButton.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				new RequestTask(true).execute();
			}
		});


		listenButton.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				new AudioSensingTask().execute();
			}
		});
	}

	class RequestTask extends AsyncTask<String, String, String>{

		JSONObject json;

		public RequestTask(boolean confirmed) {
			json = new JSONObject();
			try {
				if(confirmed)
					json.put("confirmed", "True");
				else
					json.put("confirmed", "False");
			} catch (JSONException e) {
				e.printStackTrace();
			}
		}

		@Override
		protected String doInBackground(String... uri) {
			HttpClient httpclient = new DefaultHttpClient();
			HttpResponse response;
			String responseString = null;
			try {
				HttpPost httpost = new HttpPost(DangerApplication.getApp().DANGER_SERVER_API + 
						"building_manager/confirm_danger");

				StringEntity se = new StringEntity(json.toString());

				httpost.setEntity(se);

				httpost.setHeader("Accept", "application/json");
				httpost.setHeader("Content-type", "application/json");

				response = httpclient.execute(httpost);
				StatusLine statusLine = response.getStatusLine();

				if(statusLine.getStatusCode() == HttpStatus.SC_OK){
					ByteArrayOutputStream out = new ByteArrayOutputStream();
					response.getEntity().writeTo(out);
					out.close();
					responseString = out.toString();
				} else{
					//Closes the connection.
					response.getEntity().getContent().close();
					throw new IOException(statusLine.getReasonPhrase());
				}
			} catch (ClientProtocolException e) {
				//TODO Handle problems..
			} catch (IOException e) {
				//TODO Handle problems..
			}
			return responseString;
		}

		@Override
		protected void onPostExecute(String result) {
			super.onPostExecute(result);
			//Do anything with response..
		}
	}




	/*** Audio sensing task **/
	class AudioSensingTask extends AsyncTask<String, String, String>{

		JSONObject json;


		@Override
		protected String doInBackground(String... uri) {
			HttpClient httpclient = new DefaultHttpClient();
			HttpResponse response;
			String responseString = null;
			try {
				response = httpclient.execute(new HttpGet(DangerApplication.getApp().DANGER_SERVER_API + "request_audio_sensing"));
				StatusLine statusLine = response.getStatusLine();
				if(statusLine.getStatusCode() == HttpStatus.SC_OK){
					ByteArrayOutputStream out = new ByteArrayOutputStream();
					response.getEntity().writeTo(out);
					out.close();
					responseString = out.toString();
				} else{
					//Closes the connection.
					response.getEntity().getContent().close();
					throw new IOException(statusLine.getReasonPhrase());
				}
			} catch (ClientProtocolException e) {
				//TODO Handle problems..
			} catch (IOException e) {
				//TODO Handle problems..
			}



			//Start playing when ready
			try {
				Thread.sleep(16000);
				
				if (waitForFile()) {
				
					MediaPlayer player = new MediaPlayer();
					player.setAudioStreamType(AudioManager.STREAM_MUSIC);
					player.setDataSource(DangerApplication.getApp().DANGER_SERVER_API + "download_audio_sensing");
					player.prepare();
					player.start();
				} else {
					//TODO handle
				}

			} catch (Exception e) {
				e.printStackTrace();
			}

			return responseString;
		}

		//wait for file being uploaded
		public boolean waitForFile() {
			int attemps = 0;
			
			while(attemps < 10) {
			
				HttpClient httpclient = new DefaultHttpClient();
				HttpResponse response;
				String responseString = null;
				try {
					response = httpclient.execute(new HttpGet(DangerApplication.getApp().DANGER_SERVER_API + "download_audio_sensing"));
					StatusLine statusLine = response.getStatusLine();
					if(statusLine.getStatusCode() == HttpStatus.SC_OK){
						ByteArrayOutputStream out = new ByteArrayOutputStream();
						response.getEntity().writeTo(out);
						out.close();
						responseString = out.toString();
						return true;
					} else{
						//Closes the connection.
						response.getEntity().getContent().close();
					
					}
					
					
				} catch (ClientProtocolException e) {
					//return false;
				} catch (IOException e) {
					//return false;
				} catch (Exception e) {
					//return false;
				}
				
				//wait 
				try {
					Thread.sleep(2000);
				} catch (InterruptedException e) {
					return false;
				}
				
			}
			
			return false;
		}

		@Override
		protected void onPostExecute(String result) {
			super.onPostExecute(result);

		}
	}
}
