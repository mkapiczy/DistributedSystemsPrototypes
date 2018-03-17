package DelayResponse;

/*
WARNING: THIS FILE IS AUTO-GENERATED. DO NOT MODIFY.

This file was generated from .idl using "rtiddsgen".
The rtiddsgen tool is part of the RTI Connext distribution.
For more information, type 'rtiddsgen -help' at a command shell
or consult the RTI Connext manual.
*/

import com.rti.dds.infrastructure.*;
import com.rti.dds.infrastructure.Copyable;
import java.io.Serializable;
import com.rti.dds.cdr.CdrHelper;

public class DelayResponse   implements Copyable, Serializable{

    public int msgId= 0;
    public int requestId= 0;
    public int masterTimeStamp= 0;

    public DelayResponse() {

    }
    public DelayResponse (DelayResponse other) {

        this();
        copy_from(other);
    }

    public static Object create() {

        DelayResponse self;
        self = new  DelayResponse();
        self.clear();
        return self;

    }

    public void clear() {

        msgId= 0;
        requestId= 0;
        masterTimeStamp= 0;
    }

    public boolean equals(Object o) {

        if (o == null) {
            return false;
        }        

        if(getClass() != o.getClass()) {
            return false;
        }

        DelayResponse otherObj = (DelayResponse)o;

        if(msgId != otherObj.msgId) {
            return false;
        }
        if(requestId != otherObj.requestId) {
            return false;
        }
        if(masterTimeStamp != otherObj.masterTimeStamp) {
            return false;
        }

        return true;
    }

    public int hashCode() {
        int __result = 0;
        __result += (int)msgId;
        __result += (int)requestId;
        __result += (int)masterTimeStamp;
        return __result;
    }

    /**
    * This is the implementation of the <code>Copyable</code> interface.
    * This method will perform a deep copy of <code>src</code>
    * This method could be placed into <code>DelayResponseTypeSupport</code>
    * rather than here by using the <code>-noCopyable</code> option
    * to rtiddsgen.
    * 
    * @param src The Object which contains the data to be copied.
    * @return Returns <code>this</code>.
    * @exception NullPointerException If <code>src</code> is null.
    * @exception ClassCastException If <code>src</code> is not the 
    * same type as <code>this</code>.
    * @see com.rti.dds.infrastructure.Copyable#copy_from(java.lang.Object)
    */
    public Object copy_from(Object src) {

        DelayResponse typedSrc = (DelayResponse) src;
        DelayResponse typedDst = this;

        typedDst.msgId = typedSrc.msgId;
        typedDst.requestId = typedSrc.requestId;
        typedDst.masterTimeStamp = typedSrc.masterTimeStamp;

        return this;
    }

    public String toString(){
        return toString("", 0);
    }

    public String toString(String desc, int indent) {
        StringBuffer strBuffer = new StringBuffer();        

        if (desc != null) {
            CdrHelper.printIndent(strBuffer, indent);
            strBuffer.append(desc).append(":\n");
        }

        CdrHelper.printIndent(strBuffer, indent+1);        
        strBuffer.append("msgId: ").append(msgId).append("\n");  
        CdrHelper.printIndent(strBuffer, indent+1);        
        strBuffer.append("requestId: ").append(requestId).append("\n");  
        CdrHelper.printIndent(strBuffer, indent+1);        
        strBuffer.append("masterTimeStamp: ").append(masterTimeStamp).append("\n");  

        return strBuffer.toString();
    }

}
