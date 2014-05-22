package com.danger.utilities;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import android.util.Log;

import com.google.gson.GsonBuilder;

public class RestUtils {
	private final static String METHOD_POST = "post";
	private final static String METHOD_GET= "get";
	private final static String TAG= "RestUtils";

	/***
	 * Esegue una richiesta REST
	 * 
	 * @param host   : hostname
	 * @param method  : methodo (GET,POST supportati per ora)
	 * @param path   : percorso
	 * @param parameters : parametri
	 * @return    : Stringa contenente la response
	 * @throws RestRequestException : Eccezione personalizzata
	 */
	public static String doRESTRequest (String host,  String method, String path, Map<String,String> parameters) {

		return doRESTRequest(host, "80", method, path, parameters);
	}

	/***
	 * Esegue una richiesta REST
	 * 
	 * @param host   : hostname
	 * @param port   : porta
	 * @param method  : methodo (GET,POST supportati per ora)
	 * @param path   : percorso
	 * @param parameters : parametri
	 * @return    : Stringa contenente la response
	 * @throws RestRequestException : Eccezione personalizzata
	 */
	public static String doRESTRequest (String host, String port, String method, String path, Map<String,String> parameters) {

		String returnString = null;


		String url = host+":"+port+path;
		Log.i(TAG,METHOD_GET+" Request - URL : "+url );

		if (METHOD_GET.equalsIgnoreCase(method)){
			returnString = doGETRequest(url,parameters); 
		}else if (METHOD_POST.equalsIgnoreCase(method)){
			returnString = doPOSTRequest(url, parameters);
		}
		return returnString;
	}

	/***
	 * Metodo per eseguire una request di tipo GET
	 * @param url : url della request
	 * @return  : stringa contenente la response
	 * @throws GetRequestException : Eccezione modellata
	 */
	public static String doGETRequest(String url,Map<String, String> parameters) {
		String paramStr = composeParametersForGetRequest(parameters);

		if (paramStr!=null && paramStr.length() > 0 ) url = url +"?"+paramStr;
		String websiteData = null;

		try {
			Log.i(TAG,"GetRequest - url : "+url);
			DefaultHttpClient client = new DefaultHttpClient();
			URI uri = new URI(url);
			HttpGet method = new HttpGet(uri);
			HttpResponse res = client.execute(method);
			InputStream data = res.getEntity().getContent();
			websiteData = parseISToString(data);
		} catch (ClientProtocolException e) {

		} catch (IOException e) {

		} catch (URISyntaxException e) {

		}finally{
			Log.i(TAG,"GetRequest - Request & Response completed");
		}
		return websiteData;
	}

	public static String doPOSTRequest(String url,Map<String, String> parameters) {

		String returnString = null;
		// Creo un nuovo HttpClient e l'Header del post
		String json = new GsonBuilder().create().toJson(parameters, Map.class);
		HttpClient httpclient = new DefaultHttpClient();
		HttpPost httppost = new HttpPost(url);
		try {
			httppost.setEntity(new StringEntity(json));
		} catch (UnsupportedEncodingException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		httppost.setHeader("Accept", "application/json");
		httppost.setHeader("Content-type", "application/json");
		try {
			// aggiungo i dati alla richiesta
//			List<NameValuePair> nameValuePairs = composeParametersForPostRequest(parameters);
//			httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

			// Eseguo la richiesta HTTP
			HttpResponse response = httpclient.execute(httppost);
			if (response.getStatusLine().getStatusCode() == 200) { 
				returnString = EntityUtils.toString(response.getEntity()); 
				response = null; 

			}
		} catch (ClientProtocolException e) {

		} catch (IOException e) {

		}

		return returnString;

	}

	public static List<NameValuePair> composeParametersForPostRequest(Map<String,String> parameters){

		List<String> chiavi = new ArrayList<String>(parameters.keySet());
		List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();

		for (int i = 0 ; i < chiavi.size(); i++){
			String chiave = chiavi.get(i);
			nameValuePairs.add(new BasicNameValuePair(chiave, parameters.get(chiave)));
		}

		return nameValuePairs;
	}

	/***
	 * Metodo per comporre la parte di URL relativa ai parametri
	 * @param parameters : mappa di parametri
	 * @return    : Stringa contenente i parametri concatenati
	 */
	public static String composeParametersForGetRequest(Map<String, String> parameters){
		String paramStr = "";
		List<String> chiavi = new ArrayList<String>(parameters.keySet());

		for (int i = 0 ; i < chiavi.size(); i++){
			String chiave = chiavi.get(i);
			paramStr += chiave+"=";  
			paramStr += URLEncoder.encode(parameters.get(chiave));  
			paramStr += "&";  
		}
		return paramStr;
	}

	public static String parseISToString(InputStream is){
		java.io.DataInputStream din = new java.io.DataInputStream(is);
		StringBuffer sb = new StringBuffer();
		try{
			String line = null;
			while((line=din.readLine()) != null){
				sb.append(line+"\n");
			}
		}catch(Exception ex){
			ex.getMessage();
		}finally{
			try{
				is.close();
			}catch(Exception ex){}
		}
		return sb.toString();
	}
}