package trialrun;

import java.io.IOException;
import java.net.ConnectException;
import java.net.MalformedURLException;
import java.net.SocketException;
import java.util.*;

import javax.net.ssl.SSLException;
import javax.net.ssl.SSLHandshakeException;






import org.apache.commons.httpclient.NoHttpResponseException;
import org.apache.commons.lang3.tuple.ImmutablePair;
//import org.apache.commons.math3.util.Pair;
//import org.apache.commons.lang3.tuple.ImmutablePair;
import org.apache.commons.lang3.tuple.Pair;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.HttpResponse;
//import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
//import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.util.EntityUtils;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;



import com.google.common.collect.Lists;



public class ExtractUrl {

    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(LongWritable key, Text value, OutputCollector<Text, IntWritable> output, Reporter reporter) throws ClientProtocolException, IOException {
            
        	String line = value.toString();
        	//System.out.println("value"+ value);
	       
	        //String[] command = line.split(",");
	        //int number_of_url = command.length;
	        //for(int i=0; i<number_of_url;i++)
	       	// {
	       	 //command[i]= command[i].replaceAll("[\'\\[\\]]", "").trim(); 
	       	
	       	 //if(command[i].trim().length() > 0)
	       	 //{	
        	String  originalUrl = line;
       		//System.out.println("input url " + strLine);
       		ExtractUrl link = new ExtractUrl();
       		//String newUrl= link.expandSafe(originalUrl);
       		String newUrl= link.expandSafe(originalUrl);
       		/*while(!originalUrl.equals(newUrl)){
                originalUrl=newUrl;
                if(!(newUrl=="badurl"))
                {
                newUrl=link.unshortenSingleLevel(originalUrl);
                }
                break;
            }
       		
            System.out.println("newUrl: " + newUrl);*/
          		if(newUrl!=null  &&!originalUrl.equals(newUrl)&& newUrl!="badurl"){
	                word.set(newUrl);
	                output.collect(word, one);
	       		 
	       	 //}
	       	// }
	       	 
        	
            /*ExtractUrl extract=new ExtractUrl();
            String newUrl=null;
            String originalUrl = "http://"+ value.toString().trim(); 
            String temp=originalUrl;
            System.out.println("originalUrl: " + originalUrl);

            newUrl=extract.unshortenSingleLevel(originalUrl);
            
            //if a url has multiple levels of shortening
            while(!temp.equals(newUrl)){
                temp=newUrl;
                newUrl=extract.unshortenSingleLevel(newUrl);
            }
            System.out.println("newUrl: " + newUrl);

            if(newUrl!=null && !originalUrl.equals(newUrl)){
                word.set(newUrl);
                output.collect(word, one);  */  
            }

        }
    }

   public static class Reduce extends MapReduceBase implements Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterator<IntWritable> values, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
            System.out.println("I am in Reduce");
            int sum = 0;
            while (values.hasNext()) {
                sum += values.next().get();
            }

            output.collect(key, new IntWritable(sum));
        }
    }

    public static void main(String[] args) throws Exception {
        // Configuration processed by ToolRunner
        //Configuration conf = getConf();

        // Create a JobConf using the processed conf
        JobConf job = new JobConf(ExtractUrl.class);

        // Process custom command-line options    
        Path in = new Path(args[0]); // input format in eclipse: "file:///home/cloudera/ananya/expand/input"
        Path out = new Path(args[1]);

        System.out.println("args[0] " + args[0]);
        System.out.println("args[1] " + args[1]);

        // Specify various job-specific parameters     
        job.setJobName("ExtractUrl");
        
        job.setMapperClass(Map.class);
        job.setNumReduceTasks(1);
       job.setReducerClass(Reduce.class);
        
        job.setInputFormat(TextInputFormat.class);
        job.setOutputFormat(TextOutputFormat.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        FileInputFormat.setInputPaths(job, in);
        FileOutputFormat.setOutputPath(job, out);
        

        JobClient.runJob(job);
      
    } 


   /* public  String unshortenSingleLevel(String url1) throws ClientProtocolException, IOException {
        HttpGet request=null;
         HttpParams httpParameters = new BasicHttpParams();
         httpParameters.setParameter(url1, false);
         DefaultHttpClient client = new DefaultHttpClient(httpParameters);
         ExtractUrl link = new ExtractUrl();
         String url=link.ensure_has_protocol(url1);
         HttpGet httpGet = new HttpGet(url);
     	//HttpGet request=null;

       // HttpClient client = HttpClientBuilder.create().disableRedirectHandling().build();

         try {
        	 if(!(url=="badurl"))
         	{
        	 
             request = new HttpGet(url);
             System.out.println("output url1in function " + url);
             HttpResponse httpResponse = client.execute(request);
             System.out.println("output httprequest in function " + httpResponse);

             //status code 301 : moved permanently. new location is given in the location field
             //status code 300 : found
             int statusCode = httpResponse.getStatusLine().getStatusCode();
             System.out.println("output statuscode " + statusCode);
             if (statusCode != 301 && statusCode != 302) {
                 return url;
             }
             Header[] headers = httpResponse.getHeaders(HttpHeaders.LOCATION);
             boolean checkstate = headers.length==1;
             boolean isRedirect = (statusCode == 301 || statusCode == 302 ||statusCode == 400||statusCode == 500||statusCode == 404);
             if(isRedirect)
             {
            	 System.out.println("url is invalid");
            	 return ( "badurl");
             }
             if((checkstate)){
                 String newUrl = headers[0].getValue();
                 return newUrl;
             }
             else{
                 return url;
             }
            
            	 
         }
         else {
      	   System.out.println("url is invalid");
      	   return ( "badurl");
      	}
         }
             

          catch (IllegalArgumentException ex) {
             System.err.println(ex.getMessage());
             System.err.println(ex.getStackTrace());
             return url;
         }catch (java.net.UnknownHostException ex){
             System.err.println(ex.getMessage());
             System.err.println(ex.getStackTrace());
             return url;
         }
         catch(final MalformedURLException e){
         	return "badurl";
         }
         
         catch (final SSLHandshakeException e){
         	return "badurl";	
         }
         catch (final ConnectException e){
         	return "badurl";	
         }
         catch (final SSLException e){
	        	return url;	
	        }
         catch (final SocketException e){
	        	return "badurl";	
	        }
         catch (final ClientProtocolException e){
	        	return url;	
	        }
         catch (final NoHttpResponseException e){
	        	return url;	
	        }
         catch (final IOException e){
	        	return "badurl" ;	
	        }
      
      
         finally {

             if (request != null) {
                 request.releaseConnection();
             }

         }
     }*/

    public Pair<Integer, String> expandSingleLevelSafe( String url1) throws IOException,ClientProtocolException {
	      HttpGet request=null;
	      ExtractUrl link = new ExtractUrl();
	        String url=link.ensure_has_protocol(url1);
	        HttpParams httpParameters = new BasicHttpParams();
	        //HttpEntity httpEntity = null;
	       httpParameters.setParameter("http.protocol.handle-redirects", false);
	        DefaultHttpClient client = new DefaultHttpClient(httpParameters);
	       
	      
	    	//HttpGet request=null;

	       //CloseableHttpClient client = HttpClientBuilder.create().disableRedirectHandling().build();
	       HttpGet httpGet = new HttpGet(url);

	       try {
	        	//UrlValidator urlValidator = new UrlValidator();
	        	//if (urlValidator.isValid(url)) { 
	        	if(!(url=="badurl"))
	        	{
	            request = new HttpGet(url);
	            System.out.println("output url1in function " + url);
	            
	            HttpResponse httpResponse = client.execute(request);
	            System.out.println("output httprequest in function " + httpResponse);
	           

	            //status code 301 : moved permanently. new location is given in the location field
	            //status code 300 : found
	            int statusCode = httpResponse.getStatusLine().getStatusCode();
	            System.out.println("output statuscode " + statusCode);
	            if (statusCode != 301 && statusCode != 302 ) {
	            	return new ImmutablePair<Integer, String>(statusCode, url);
	            }
	            Header[] headers = httpResponse.getHeaders(HttpHeaders.LOCATION);
	            //boolean checkstate = headers.length==1;
	       
		        Preconditions.checkState(headers.length==1);
		        String newUrl = headers[0].getValue();
		        return new ImmutablePair<Integer, String>(statusCode, newUrl);
	        }
	        else {
       	   System.out.println("url is invalid");
       	   return new ImmutablePair<Integer, String>(500, url);
	        }
	            
	        } catch (IllegalArgumentException ex) {
	            System.err.println(ex.getMessage());
	            System.err.println(ex.getStackTrace());
	            return new ImmutablePair<Integer, String>(500, url); 
	            
	        }catch (java.net.UnknownHostException ex){
	            System.err.println(ex.getMessage());
	            System.err.println(ex.getStackTrace());
	            return new ImmutablePair<Integer, String>(500, url); 
	        }
	        catch(final MalformedURLException e){
	        	 return new ImmutablePair<Integer, String>(500, "badurl");
	        }
	        catch (final SSLHandshakeException e){
 	        	return new ImmutablePair<Integer, String>(500, "badurl");	
 	        }
	        
	        catch (final ConnectException e){
	         	return new ImmutablePair<Integer, String>(500, "badurl");
	         }
	         catch (final SSLException e){
		        	 return new ImmutablePair<Integer, String>(500, "badurl");
		        }
	         catch (final SocketException e){
	        	 return new ImmutablePair<Integer, String>(500, "badurl");	
		        }
	         catch (final ClientProtocolException e){
	        	 return new ImmutablePair<Integer, String>(500, "badurl");
	        	 
		        }
	         catch (final NoHttpResponseException e){
	        	 return new ImmutablePair<Integer, String>(500, "badurl");
		        }
	         catch (final IOException e){
	        	 return new ImmutablePair<Integer, String>(500, "badurl");
		        }
	        
	        
         
	      
	      
	 	      
	        finally {

	            if (request != null) {
	                request.releaseConnection();
	            }
	            

	        }
	    }
	        public  String expandSafe( String urlArg) throws IOException,ClientProtocolException { 
	        		String originalUrl = urlArg; 
	        		ExtractUrl link = new ExtractUrl();
	        		String newUrl = link.expandSingleLevelSafe(originalUrl).getRight(); 
	        		final List<String> alreadyVisited = Lists.newArrayList(originalUrl, newUrl); 
	        		
	        	 		while (!originalUrl.equals(newUrl)) { 
	        	 			if (newUrl!="badurl")
	        	 			{
	        	 			originalUrl = newUrl; 
	        	 			 Pair<Integer, String> statusAndUrl = link.expandSingleLevelSafe(originalUrl); 
	        	 			newUrl = statusAndUrl.getRight(); 
	        	 			boolean loophole = statusAndUrl.getLeft() == 404 || statusAndUrl.getLeft() == 200|| statusAndUrl.getLeft() == 400; 
	        	 			if (loophole) { 
	        					return "badurl";
	        	 			}
	        	 			
	        	 			 boolean isRedirect = statusAndUrl.getLeft() == 301 || statusAndUrl.getLeft() == 302; 
	        	 			if (isRedirect && alreadyVisited.contains(newUrl)) { 
	        					throw new IllegalStateException("Likely a redirect loop"); 
	        	 			} 
	        	 			alreadyVisited.add(newUrl); 
	        	 			}
	        	 			break;
	        	 		} 
	        	 		
    	 			
	        	 
	        	 
	        	 		return newUrl; 
	       	} 
	        
	        public String ensure_has_protocol(final String a_url)
	        {
	            if (!a_url.startsWith("http://"))
	            {	
	            	 if (!a_url.startsWith("https://"))
	            	 { if (!(a_url.length()<10))
	            	 		{
	            		 return "http:/" + a_url;
	            	 		}
	            	 }
	            	 else  
	            		 {if (!(a_url.length()<10))
	            			 return   a_url;
	            		 }
	            }
	            System.out.println(a_url.length());
	            if (!(a_url.length()<10))
    	 		{
	            	return  a_url;
    	 		}
	            return "badurl";
	        }

    
    public final class Preconditions {

    	public  void checkState(boolean expression){
    		if(!expression){
    			throw new IllegalStateException();
    		}
    	}
    }
}

	
