
from math import sqrt

def inBoundary(dt, e1, r1):
    """ returns a bool indicating if the entitiy is in the rect over the timestep dt """
    try:
            return _inBoundaryForAccel(dt, e1, r1)
    except AttributeError:
        try:
            return _inBoundaryForVel(dt, e1, r1)
        except AttributeError:
            try:
                return _inBoundaryForPos(dt, e1, r1)
            except AttributeError:
                return False

def _inBoundaryForAccel(dt, e1, r1):
    # x1 = x10 + vx1*dt*lx + 1/2*ax1*dt^2*lx**2
    # x2 = x20 + vx2*dt*lx + 1/2*ax2*dt^2*lx**2
    # x1 = x2 => 0 = dx0 + dvx*dt*l + 1/2*dax*dt**2*l**2
    # => lx = (-dvx*dt +- sqrt((dvx*dt)**2 - 4*1/2*dax*dt**2*dx0))/(dax*dt**2))

    dax = e1.state.accelerationComponent.ax 
    day = e1.state.accelerationComponent.ay 
    
    dvx = e1.state.velocityComponent.vx 
    dvy = e1.state.velocityComponent.vy
    
    dx0_r = e1.state.geometryComponent.location[0] + e1.state.geometryComponent.width - r1.left
    dx0_l = e1.state.geometryComponent.location[0] - r1.right
    dy0_t = e1.state.geometryComponent.location[1] - r1.bottom
    dy0_b = e1.state.geometryComponent.location[0] + e1.state.geometryComponent.height - r1.top
     


    dis_r = (dvx*dt)**2 - 2*dax*dt**2*dx0_r
    if dis_r > 0:
        lx_1r = (-dvx*dt + sqrt(dis_r))/(dax*dt**2)
        lx_2r = (-dvx*dt - sqrt(dis_r))/(dax*dt**2)
        lx_1r, lx_2r = min(lx_1r, lx_2r), max(lx_1r, lx_2r)
    
    dis_l = (dvx*dt)**2 - 2*dax*dt**2*dx0_l
    if dis_l > 0:
        lx_1l = (-dvx*dt + sqrt(dis_l))/(dax*dt**2)
        lx_2l = (-dvx*dt - sqrt(dis_l))/(dax*dt**2)
        lx_1l, lx_2l = min(lx_1l, lx_2l), max(lx_1l, lx_2l)

    
    dis_t = (dvy*dt)**2 - 2*day*dt**2*dy0_t
    if dis_t > 0:
        ly_1t = (-dvy*dt + sqrt(dis_t))/(day*dt**2)
        ly_2t = (-dvy*dt - sqrt(dis_t))/(day*dt**2)
        ly_1t, ly_2t = min(ly_1t, ly_2t), max(ly_1t, ly_2t)

        
    dis_b = (dvy*dt)**2 - 2*day*dt**2*dy0_b
    if dis_b > 0:
        ly_1b = (-dvy*dt + sqrt(dis_b))/(day*dt**2)
        ly_2b = (-dvy*dt - sqrt(dis_b))/(day*dt**2)
        ly_1b, ly_2b = min(ly_1b, ly_2b), max(ly_1b, ly_2b)
    
    lx = []
    if dis_r > 0 and dis_l >0:
        temp = (max(0,min(lx_1r, lx_1l)), min(1,max(lx_1r, lx_1l)))
        if temp[0] < temp[1]:
            lx.append(temp)
        temp = (max(0,min(lx_2r, lx_2l)), min(1,max(lx_2r, lx_2l)))
        if temp[0] < temp[1]:
            lx.append(temp)
    elif dis_r >0:
        temp = (max(0,min(lx_1r, lx_2r)), min(1,max(lx_1r, lx_2r)))
        if temp[0] < temp[1]:
            lx.append(temp)
    else:
        temp = (max(0,min(lx_1l, lx_2l)), min(1,max(lx_1l, lx_2l)))
        if temp[0] < temp[1]:
            lx.append(temp)
    
    ly = []
    if dis_t > 0 and dis_b >0:
        temp = (max(0,min(ly_1t, ly_1b)), min(1,max(ly_1t, ly_1b)))
        if temp[0] < temp[1]:
            ly.append(temp)
        temp = (max(0,min(ly_2t, ly_2b)), min(1,max(ly_2t, ly_2b)))
        if temp[0] < temp[1]:
            ly.append(temp)
    elif dis_t >0:
        temp = (max(0,min(ly_1t, ly_2t)), min(1,max(ly_1t, ly_2t)))
        if temp[0] < temp[1]:
            ly.append(temp)
    else:
        temp = (max(0,min(ly_1b, ly_2b)), min(1,max(ly_1b, ly_2b)))
        if temp[0] < temp[1]:
            ly.append(temp)
    
    #find the intersection of dl and [0,1]
    #if intersection l_1 < l_2 else l_2 < l_1
    
    for l1, l2 in lx, ly:
        if l1[0] < l2[0] < l1[1]:
            return True
        if l2[0] < l1[0] < l2[1]:
            return True
    
    return False

def _inBoundaryForVel(dt, e1, r1):
    # x1 = x10 + vx1*dt*lx 
    # x2 = x20 + vx2*dt*lx
    # x1 = x2 => 0 = dx0 + dvx*dt*lx 
    # => lx = -dx0 / (dvx*dt)

    dvx = e1.state.velocityComponent.vx
    dvy = e1.state.velocityComponent.vy
    
    dx0_r = e1.state.geometryComponent.location[0] + e1.state.geometryComponent.width - r1.left
    dx0_l = e1.state.geometryComponent.location[0] - r1.right
    dy0_t = e1.state.geometryComponent.location[1] - r1.bottom
    dy0_b = e1.state.geometryComponent.location[0] + e1.state.geometryComponent.height - r1.top
    
    lx_1 = -dx0_r / (dvx*dt)
    lx_2 = -dx0_l / (dvx*dt)
    ly_1 = -dy0_t / (dvy*dt)
    ly_2 = -dy0_b / (dvy*dt)
    
    lx_1, lx_2 = min(lx_1, lx_2), max(lx_1, lx_2)
    ly_1, ly_2 = min(ly_1, ly_2), max(ly_1, ly_2)
    
    return True if lx_1 < ly_1 < lx_2 or ly_1 < lx_1 < ly_2 else False

def _inBoundaryForPos(dt, e1, r1):
    return True if e1.state.geometryComponent.location[0] < r1.left < e1.state.geometryComponent.location[0] + e1.state.geometryComponent.width or r1.left < e1.state.geometryComponent.location[0] < r1.right else False
    
    