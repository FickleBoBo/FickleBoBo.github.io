import io.MyFileReader;

import java.io.BufferedReader;
import java.io.IOException;

public class TryWithResourcesV2 {

    public static void main(String[] args) throws IOException {
        System.out.println(testV1("resources/data.dat"));
        // FileReader 생성 = io.MyFileReader@10f87f48
        // catch 블럭
        // reader close() 호출 전
        // reader close() 호출 후
        // testV1 .dat 파일 확장자 예외
        // -> catch 블럭 수행 후 finally 블럭에서 자원 반납

        System.out.println(testV2("resources/data.dat"));
        // FileReader 생성 = io.MyFileReader@10f87f48
        // reader close() 호출 전
        // reader close() 호출 후
        // catch 블럭
        // testV2 .dat 파일 확장자 예외
        // -> close 메서드를 먼저 호출하고 catch 블럭 수행
    }

    static String testV1(String path) throws IOException {
        BufferedReader br = new BufferedReader(new MyFileReader(path));

        try {
            // .dat 확장자면 예외를 던짐
            if (path.endsWith(".dat")) {
                throw new IOException("testV1 .dat 파일 확장자 예외");
            }

            return br.readLine();
        } catch (IOException e) {
            System.out.println("catch 블럭");
            return e.getMessage();
        } finally {
            // 자원 회수
            br.close();
        }
    }

    static String testV2(String path) {
        try (BufferedReader br = new BufferedReader(new MyFileReader(path))) {
            // .dat 확장자면 예외를 던짐
            if (path.endsWith(".dat")) {
                throw new IOException("testV2 .dat 파일 확장자 예외");
            }

            return br.readLine();
        } catch (IOException e) {
            System.out.println("catch 블럭");
            return e.getMessage();
        }
    }
}
