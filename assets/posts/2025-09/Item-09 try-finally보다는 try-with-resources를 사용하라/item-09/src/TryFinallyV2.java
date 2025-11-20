import io.MyFileReader;
import io.MyFileWriter;
import io.MyFileWriter2;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;

public class TryFinallyV2 {

    public static void main(String[] args) {
        try {
            System.out.println(copyV1("resources/data.txt", "resources/dataV1.txt"));
            // FileReader 생성 = io.MyFileReader@10f87f48
            // FileWriter 생성 = io.MyFileWriter@7291c18f
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // ok
        } catch (IOException e) {
            e.printStackTrace();
        }

        try {
            System.out.println(copyV1("resources/data.dat", "resources/dataV1.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@7cc355be
            // FileWriter 생성 = io.MyFileWriter@6e8cf4c6
            // writer close() 호출 전
            // writer close() 호출 후
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: copyV1 .dat 파일 확장자 예외
            //     at TryFinallyV2.copyV1(TryFinallyV2.java:70)
            //     at TryFinallyV2.main(TryFinallyV2.java:26)
            // -> 예외가 터졌지만 자원 회수 성공
        }

        try {
            System.out.println(copyV2("resources/data.dat", "resources/dataV2.dat"));
        } catch (IOException e) {
            e.printStackTrace();
            // FileReader 생성 = io.MyFileReader@27973e9b
            // FileWriter 생성 = io.MyFileWriter2@7530d0a
            // writer close() 호출 전2
            // reader close() 호출 전
            // reader close() 호출 후
            // java.io.IOException: writer close 호출 중 예외 발생
            //     at io.MyFileWriter2.close(MyFileWriter2.java:16)
            //     at java.base/java.io.BufferedWriter.implClose(BufferedWriter.java:398)
            //     at java.base/java.io.BufferedWriter.close(BufferedWriter.java:386)
            //     at TryFinallyV2.copyV2(TryFinallyV2.java:100)
            //     at TryFinallyV2.main(TryFinallyV2.java:42)
            // -> 예외는 finally 블럭에서도 발생할 수 있으며 핵심 예외인 파일 확장자 예외가 writer 자원 회수 실패 예외에 덮혀짐
        }
    }

    // 중첩된 try-finally 블록으로 코드가 복잡해진다(자원의 생명주기도 고려해야 한다)
    static String copyV1(String src, String dst) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(src));

        try {
            BufferedWriter bw = new BufferedWriter(new MyFileWriter(dst));

            try {
                // .dat 확장자면 예외를 던짐
                if (src.endsWith(".dat")) {
                    throw new IOException("copyV1 .dat 파일 확장자 예외");
                }

                String line;
                while ((line = br.readLine()) != null) {
                    bw.write(line);
                }
                return "ok";
            } finally {
                bw.close();
            }
        } finally {
            br.close();
        }
    }

    static String copyV2(String src, String dst) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(src));

        try {
            BufferedWriter bw = new BufferedWriter(new MyFileWriter2(dst));

            try {
                // .dat 확장자면 예외를 던짐
                if (src.endsWith(".dat")) {
                    throw new IOException("copyV2 .dat 파일 확장자 예외");
                }

                String line;
                while ((line = br.readLine()) != null) {
                    bw.write(line);
                }
                return "ok";
            } finally {
                bw.close();
            }
        } finally {
            br.close();
        }
    }
}
