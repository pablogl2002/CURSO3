import java.util.concurrent.locks.*;

/**
 * Write a description of class Terrain2 here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */

public class Terrain2 implements Terrain {
    Viewer v;
    Lock mutex;
    Condition c[][];
    
    public  Terrain2 (int t, int ants, int movs, String msg) {
        v=new Viewer(t,ants,movs,msg);
        mutex = new ReentrantLock();
        c = new Condition[t][t];
        for (int i = 0; i < t; i++) 
            for (int j = 0; j < t; t++)
                c[i][j] = mutex.newCondition();

    }
    public void     hi      (int a) {
        try {
            mutex.lock();
            v.hi(a);
        } finally { mutex.unlock(); }
    }
    public void     bye     (int a) {
        try {
            mutex.lock();
            Pos p = v.getPos(a);
            c[p.x][p.y].signalAll();
            v.bye(a);
        } finally {
            mutex.unlock();
        }
    }
    public void     move    (int a) throws InterruptedException {
        try {
            mutex.lock();
            v.turn(a); Pos dest=v.dest(a); 
            while (v.occupied(dest)) {wait(); v.retry(a);}
            v.go(a);
            Pos p = v.getPos(a);
            c[p.x][p.y].signalAll();
        } finally {
            mutex.unlock();
        }
    }
}
