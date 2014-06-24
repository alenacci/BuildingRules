package com.hpps.danger.user;

import java.io.File;
import java.io.IOException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Environment;
import android.os.Handler;
import android.util.Log;
import android.webkit.MimeTypeMap;
import android.widget.Toast;

import com.hpps.danger.DangerApplication;

public class AudioSensing {

	public final int REC_DURATION =10000;
	private MediaRecorder mRecorder = null;
	private static String mFileName = null;

	public AudioSensing() {
		mFileName = Environment.getExternalStorageDirectory().getAbsolutePath();
		mFileName += "/audiorecordtest.3gp";
	}

	public void start() {
		//Show a toast
		Handler h = new Handler(DangerApplication.getApp().getMainLooper());

	    h.post(new Runnable() {
	        @Override
	        public void run() {
	             Toast.makeText(DangerApplication.getApp(),"Start recording",Toast.LENGTH_LONG).show();
	        }
	    });
	    
	    //Start recording
		(new RecordTask()).execute();


	}

	class RecordTask extends AsyncTask<String, String, String>{

		public RecordTask() {

		}

		@Override
		protected String doInBackground(String... uri) {
			startRecording();
			try {
				Thread.sleep(REC_DURATION);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			stopRecording();
			uploadRecording();
			return null;
		}

		@Override
		protected void onPostExecute(String result) {

		}

		private void startRecording() {
			mRecorder = new MediaRecorder();
			mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
			mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
			mRecorder.setOutputFile(mFileName);
			mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

			try {
				mRecorder.prepare();
			} catch (IOException e) {
				Log.e("ERROR", "prepare() failed");
			}

			mRecorder.start();
		}

		private void stopRecording() {
			mRecorder.stop();
			mRecorder.release();
			mRecorder = null;
		}

		private void uploadRecording() {
			String DANGER_SERVER_API = DangerApplication.getApp().DANGER_SERVER_API;
			String url = DANGER_SERVER_API + "user/upload_audio";

			String extStorage = Environment.getExternalStorageDirectory()
					.getAbsolutePath();
			
			//Access file
			final File file = new File(mFileName);
//			final File file = new File(extStorage + "/a.jpg");
			long size = file.length();

			try
			{
				HttpClient client = new DefaultHttpClient();

				HttpPost post = new HttpPost(url);
//				post.setHeader( "Content-Type", "multipart/form-data" );
				
				MultipartEntityBuilder entityBuilder = MultipartEntityBuilder.create();

				String mime = MimeTypeMap.getSingleton().getMimeTypeFromExtension("3gp");
				//entityBuilder.setMode(HttpMultipartMode.BROWSER_COMPATIBLE);

				//entityBuilder.addTextBody("user", "andre");
				//entityBuilder.add

				if(file != null)
				{
					entityBuilder.addPart("file", new FileBody(file));
					//entityBuilder.addBinaryBody("file", file);
				}

				HttpEntity entity = entityBuilder.build();

				post.setEntity(entity);

				HttpResponse response = client.execute(post);

				HttpEntity httpEntity = response.getEntity();

				String result = EntityUtils.toString(httpEntity);

				Log.v("UPLOAD", "http audio upload" + result);
			}
			catch(Exception e)
			{
				e.printStackTrace();
			}
		}
	}

}
