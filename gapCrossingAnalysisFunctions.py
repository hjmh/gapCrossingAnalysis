import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

### Plotting functions
def plotClimbingVector(gtdata, ax, gapsize, arrowCol):
    gs = list(np.squeeze(np.asarray(gtdata[8])))
    
    if gapsize < 0:
        mask = np.arange(len(gs))
    else:
        mask = np.where(gs == gapsize)[0]
        
    #select data of from experiment with correct gap size
    xa = np.squeeze(np.asarray(gtdata[3]))[mask]
    xh = np.squeeze(np.asarray(gtdata[4]))[mask]
    ya = -np.squeeze(np.asarray(gtdata[5]))[mask]
    yh = -np.squeeze(np.asarray(gtdata[6]))[mask]
    
    for k in range(len(xa)):
        arrow = FancyArrow(xa[k], ya[k], xh[k]-xa[k], yh[k]-ya[k], width=0.04, 
                      color=arrowCol, length_includes_head=True, head_width=0.25, alpha=0.7)
        ax.add_patch(arrow)
    
    # add visual indicator for platform
    drawBlock(ax, gapsize)

    
def drawBlock(ax, gapsize):
    rect1 = Rectangle((-6,-4), 6, 4, color='grey', alpha=0.3)
    ax.add_patch(rect1)

    if gapsize >0: 
        rect2 = Rectangle((0+gapsize,-4), 6, 4, color='grey', alpha=0.3)
        ax.add_patch(rect2)


##Axis beautification

def myAxisTheme(myax):
    myax.get_xaxis().tick_bottom()
    myax.get_yaxis().tick_left()
    myax.spines['top'].set_visible(False)
    myax.spines['right'].set_visible(False)
    
def reducedAxis(myax, scalebar, unit):
    myax.axis('off')
    myax.axis('equal')
    
    #plot scale bar instead
    barlen = scalebar[2]
    myax.plot([scalebar[1],scalebar[1]+barlen],[scalebar[0],scalebar[0]], linewidth=2, color='k')
    myax.text(scalebar[1]+0.25*barlen,scalebar[0]+0.1*barlen, str(barlen)+' '+unit)
    
### Circular measures

def _circfuncs_common(samples, high, low):
    # Modified function circmean from scipy.stats package.
    if samples.size == 0:
        return np.nan, np.nan

    ang = (samples - low)*2*np.pi / (high - low)
    return samples, ang

def circmeanvec(samples, weights, high=2*np.pi, low=0, axis=None):
    # Modified function circmean from scipy.stats package. Added calculation of mean vector length
    """
    Compute the circular mean for samples in a range.
    Parameters
    ----------
    samples : array_like
        Input array.
    weights: array_like
        Input array with weights (i.e. vector lengths)
    high : float or int, optional
        High boundary for circular mean range.  Default is ``2*pi``.
    low : float or int, optional
        Low boundary for circular mean range.  Default is 0.
    axis : int, optional
        Axis along which means are computed.  The default is to compute
        the mean of the flattened array.
    Returns
    -------
    circmean : float
        Circular mean direction
        Ciruclar mean length
    """
    samples, ang = _circfuncs_common(samples, high, low)

    try:
        N = len(ang)
    except:
        print('problem with sample')
        print(samples)

        return np.nan, np.nan

    S = (weights*np.sin(ang)).sum(axis=axis)
    C = (weights*np.cos(ang)).sum(axis=axis)
    res = np.arctan2(S, C)
    mask = res < 0
    if mask.ndim > 0:
        res[mask] += 2*np.pi
    elif mask:
        res += 2*np.pi
    direction = res*(high - low)/2.0/np.pi + low

    length = np.sqrt(np.square(C) + np.square(S))/len(weights)

    return direction, length