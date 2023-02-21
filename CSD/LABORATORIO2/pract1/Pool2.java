// CSD feb 2015 Juansa Sendra

public class Pool2 extends Pool{ //max kids/instructor
    int nInst = 0;
    int nKids = 0;
    int mki = 2;
    
    public void init(int ki, int cap)           {
        mki = ki;
    }
    public synchronized void kidSwims() throws InterruptedException {
        while (nInst <= 0 || nKids >= mki * nInst) {
            log.waitingToSwim();
            wait();
        }
        nKids++;
        notifyAll();
        log.swimming();
    }
    public synchronized void kidRests()      {
        nKids--;
        log.resting();
        notifyAll();
    }
    public synchronized void instructorSwims()   {
        nInst++;
        log.swimming();
        notifyAll();
    }
    public synchronized void instructorRests() throws InterruptedException {
        while (nKids > mki * (nInst - 1) && nInst > 0) {
            log.waitingToRest();
            wait();
        }
        nInst--;
        log.resting();
        notifyAll();
    }
}
